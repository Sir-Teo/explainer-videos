from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, ITO, JUMP, PART, STRAT, load

NOISE = QC.REALIZED


class Research(VoiceoverScene):
    def construct(self):
        t = load("rv_theory")
        self.card()
        self.theorem()
        self.proof()
        self.coverage(t)
        self.noise_(t)
        self.jumps(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The error in realized variance", r"How well can a day's volatility be measured from its "
                          r"prices?", part=PART)
        with self.voiceover("For the researcher: Chapter 2 measured quadratic variation from prices sampled finer and "
                            "finer. How well, exactly? The answer is a central limit theorem, and two ways it breaks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        thm = theorem_card(r"A central limit theorem for realized variance", VGroup(
            MathTex(r"dX_t = \sigma_t\,dW_t,\qquad \mathrm{RV}_n = \textstyle\sum_{i=1}^n (X_{i/n} - X_{(i-1)/n})^2", font_size=30),
            MathTex(r"\sqrt n\,\Big(\mathrm{RV}_n - \textstyle\int_0^1\sigma_s^2\,ds\Big)\ \xrightarrow{\ \text{stably}\ }\ "
                    r"\mathcal{MN}\Big(0,\ 2\textstyle\int_0^1\sigma_s^4\,ds\Big)", font_size=30),
            MathTex(r"\frac{\mathrm{RV}_n - \mathrm{IV}}{\sqrt{2\,\mathrm{RQ}_n/n}} \Rightarrow N(0, 1),\quad \mathrm{RQ}_n = "
                    r"\tfrac n3\textstyle\sum (\Delta_i X)^4", font_size=30, color=ITO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25), who=r"Jacod (1994); Barndorff-Nielsen and Shephard (2002)", width=11.4,
            font_size=24).move_to(UP * 0.2)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> Sample a continuous price n times a day and add up the squared returns. "
            "The error against the day's integrated variance shrinks like one over root n, and tends to a mixed "
            "normal: normal given the volatility path, with a variance of twice the integrated quarticity, the "
            "integral of sigma to the fourth. <bookmark mark='b'/> The quarticity is itself estimated from the fourth "
            "powers of the returns, and the studentized error is then a plain standard normal. So a realized variance "
            "comes with a standard error, computed from the same day's data."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(Indicate(thm, color=ITO, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\mathrm{RV}_n - \mathrm{IV}", r"=", r"\textstyle\sum_i \xi_i,\quad \xi_i = (\Delta_i X)^2 - \int_{t_{i-1}}"
                      r"^{t_i}\sigma_s^2 ds", font_size=30, colors={r"\mathrm{RV}_n - \mathrm{IV}": ITO}),
                cmath(r"\mathbb E[\xi_i \mid \mathcal F_{t_{i-1}}]", r"=", r"0", font_size=30,
                      colors={r"\mathbb E[\xi_i \mid \mathcal F_{t_{i-1}}]": BM}),
                cmath(r"\mathbb E[\xi_i^2 \mid \mathcal F_{t_{i-1}}]", r"\approx", r"2\,\sigma_{t_{i-1}}^4/n^2", font_size=30,
                      colors={r"\mathbb E[\xi_i^2 \mid \mathcal F_{t_{i-1}}]": BM}),
                cmath(r"n\textstyle\sum_i \mathbb E[\xi_i^2 \mid \mathcal F_{t_{i-1}}]", r"\to", r"2\textstyle\int_0^1\sigma_s^4 ds",
                      font_size=30, colors={r"n\textstyle\sum_i \mathbb E[\xi_i^2 \mid \mathcal F_{t_{i-1}}]": ITO})]
        whys = [why(r"the error is a sum of one term per interval: the squared return less the variance that accrued in it"),
                why(r"Itô's isometry (Chapter 3): each term has conditional mean zero, so the sum is a martingale"),
                why(r"over a short interval the return is nearly normal with variance $\sigma^2/n$, and a centred "
                    r"$\chi^2_1$ has variance two"),
                why(r"a Riemann sum; the martingale central limit theorem then gives the mixed normal, with convergence "
                    r"stable so that the random variance may be estimated (Jacod and Shiryaev)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The proof is Part 5's machinery again. <bookmark mark='a'/> Write the error as a sum over intervals: each "
            "squared return, less the variance that accrued in it. <bookmark mark='b'/> By Itô's isometry each term has "
            "conditional mean zero, so the sum is a martingale. <bookmark mark='c'/> Over a short interval the return "
            "is close to normal, so its square, centred, has variance two sigma to the fourth over n squared. "
            "<bookmark mark='d'/> Add these up, scale by n, and the Riemann sum tends to twice the integrated "
            "quarticity. The martingale central limit theorem gives the mixed normal, and because the convergence is "
            "stable, the random variance may be replaced by its estimate."
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

    def coverage(self, t):
        ns = t["ns"]
        lab = {39: r"10 min", 78: r"5 min", 390: r"1 min", 2340: r"10 s", 23400: r"1 s"}
        hx = [-3.6, -0.6, 1.8, 4.4]
        head = VGroup(label(r"sampling", font_size=18, color=GREY_B), label(r"95\% interval covers", font_size=18),
                      label(r"sd of studentized error", font_size=18), label(r"relative error, sd", font_size=18))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(rf"{lab[n]} ($n = {n}$)".replace("23400", "23{,}400").replace("2340", "2{,}340"),
                                                       font_size=18, color=BM),
                                                 MathTex(rf"{100 * t['clt'][str(n)]['cover95']:.1f}\%", font_size=24),
                                                 MathTex(rf"{t['clt'][str(n)]['sd_t']:.2f}", font_size=24),
                                                 MathTex(rf"{100 * t['clt'][str(n)]['rel_sd']:.1f}\%", font_size=24))
                                          for n in ns]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.62 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.4, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(rf"{t['M']} simulated days of 23{{,}}400 one-second steps: 30\% annual volatility, a U-shaped "
                             r"intraday pattern and a log-normal volatility path; no noise, no jumps. The theorem's "
                             r"interval is honest at every frequency, and the error falls like $1/\sqrt n$", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Check it on three thousand simulated days, each with clustering volatility and a U-shaped intraday "
            "pattern. <bookmark mark='a'/> At ten-minute sampling, thirty-nine returns a day, the ninety-five percent "
            "interval covers eighty-nine percent of days: the asymptotics have not quite arrived, and the studentized "
            "error is a little too wide. At five minutes it covers ninety-two; at one minute ninety-four; at ten "
            "seconds and at one second, ninety-five. And the error itself falls like one over root n, from "
            "twenty-seven percent of the day's variance at ten minutes to about one percent at one second."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def noise_(self, t):
        ns = t["ns"]
        nz = t["noise"]
        x = np.log10(np.asarray(ns, float))
        y = np.asarray([nz["rv_over_iv"][str(n)] for n in ns])
        yt = 1 + np.asarray([nz["bias_theory"][str(n)] for n in ns])
        top = float(max(y.max(), yt.max()) * 1.1)
        g = axes([1.4, 4.5], [0, top], x_length=7.6, y_length=4.0, xlabel=r"returns per day, $n$",
                 ylabel=r"mean $\mathrm{RV}_n / \mathrm{IV}$, with noise", xticks=[2, 3, 4], yticks=[1, 5, 10, 15],
                 font_size=13, log_x=True).move_to(LEFT * 1.6 + DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=NOISE) for a, b in zip(x, y)])
        th = curve(ax, x, yt, WHITE, stroke_width=2)
        one = DashedLine(ax.c2p(1.4, 1), ax.c2p(4.5, 1), color=GREY_B, stroke_width=1.5)
        rows = VGroup(
            MathTex(r"Y_{t_i} = X_{t_i} + \varepsilon_i,\ \ \varepsilon_i \sim (0, \omega^2)", font_size=26),
            MathTex(r"\mathbb E\,\mathrm{RV}_n(Y) = \mathrm{IV} + 2n\omega^2", font_size=26, color=NOISE),
            MathTex(rf"\text{{TSRV}}:\ {nz['tsrv_mean']:.2f} \pm {nz['tsrv_sd']:.2f}\ \times \mathrm{{IV}}", font_size=24,
                    color=ITO),
            MathTex(rf"\text{{5-min RV}}:\ {nz['rv5_mean']:.2f} \pm {nz['rv5_sd']:.2f}\ \times \mathrm{{IV}}", font_size=24),
            wrapped_label(rf"noise of {t['omega'] * 1e4:.0f} basis points on each observed price; white: "
                          r"$1 + 2n\omega^2/\mathrm{IV}$. Zhang, Mykland and A\"it-Sahalia's (2005) two-scales estimator "
                          r"averages sparse grids and subtracts the dense one's bias", 3.8, 14, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        fit_right(rows)
        with self.voiceover(
            "The first way it breaks: real prices are not the efficient price. <bookmark mark='a'/> Add noise, bid-ask "
            "bounce and discreteness, to every observed price. Each return now carries two noise terms, and their "
            "squares do not average away: the expected realized variance is the true one plus two n omega squared, "
            "which grows without bound as you sample faster. <bookmark mark='b'/> The dots are the simulation, the "
            "white line the formula, and they agree to the third digit. At one-second sampling with five basis points of "
            "noise, realized variance is forty-three times the truth; even at five minutes it is fourteen percent too "
            "high. <bookmark mark='c'/> Zhang, Mykland and Aït-Sahalia's two-scales "
            "estimator averages realized variances on several sparse grids and subtracts the dense grid's bias, and "
            "recovers the true variance from the noisy one-second prices."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(rows[:2]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(th), LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in dots], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.wait(0.4)
        self.clear_scene()

    def jumps(self, t):
        j = t["jumps"]
        rows = [cmath(r"\mathrm{RV}_n", r"\to", r"\textstyle\int\sigma^2 + \sum_{s \le 1}(\Delta X_s)^2", font_size=32,
                      colors={r"\mathrm{RV}_n": JUMP}),
                cmath(r"\mathrm{BV}_n", r"=", r"\tfrac\pi2\textstyle\sum |\Delta_i X||\Delta_{i-1}X| \to \int\sigma^2", font_size=32,
                      colors={r"\mathrm{BV}_n": ITO}),
                cmath(r"z", r"=", r"\frac{(\mathrm{RV} - \mathrm{BV})/\mathrm{RV}}{\sqrt{(\tfrac{\pi^2}{4} + \pi - 5)\,"
                      r"\max(1, \mathrm{TQ}/\mathrm{BV}^2)/n}}", font_size=30, colors={r"z": STRAT})]
        whys = [why(r"the second way it breaks: realized variance also collects every jump's square"),
                why(r"Barndorff-Nielsen and Shephard (2004): products of neighbouring absolute returns ignore a single jump, "
                    r"since its neighbours are small"),
                why(r"Huang and Tauchen (2005): the share of variance from jumps, studentized with tripower quarticity "
                    r"TQ; reject 'no jump' when $z > 1.645$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        res = VGroup(
            MathTex(rf"\text{{no jump}}:\ \text{{rejects}}\ {100 * j['none']['reject']:.1f}\%", font_size=28, color=ITO),
            MathTex(rf"\text{{one 1\% jump}}:\ \text{{rejects}}\ {100 * j['jump']['reject']:.1f}\%", font_size=28, color=JUMP),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The second way it breaks is a jump. <bookmark mark='a'/> Realized variance collects the square of every "
            "jump on top of the integrated variance. <bookmark mark='b'/> Bipower variation, the sum of products of "
            "neighbouring absolute returns, ignores a lone jump, because its neighbours are small; it estimates the "
            "continuous part alone. <bookmark mark='c'/> The gap between the two, studentized, is Huang and Tauchen's "
            "test. On five-minute returns it rejects 'no jump' on about ten percent of the days that have none, twice "
            "its nominal five percent, because volatility moves within the day; and on half of the days with one "
            "jump of one percent. A jump smaller than the day's continuous moves is hard to see at five minutes."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(res))
        self.wait(0.5)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: noise that is not white", r"the optimal rate with noise is $n^{-1/4}$ (pre-averaging, "
                          r"realized kernels, quasi-likelihood); with noise correlated with returns, irregular trading times "
                          r"and price discreteness, which estimator is efficient is still open", width=12.4, font_size=18),
            desk_question(r"open: spot volatility when volatility is rough", r"Part 14's rough volatility makes the "
                          r"variance path nearly as irregular as the price; estimating $\sigma_t$ itself, not its integral, "
                          r"converges very slowly and the right rates are debated", width=12.4, font_size=18),
            desk_question(r"open: jumps in volatility, and co-jumps", r"telling a jump in the price from a jump in its "
                          r"volatility, and jumps common to many assets, with finite data", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With noise the best possible rate is one over n to the quarter, "
            "and several estimators reach it, but when the noise is correlated with returns and trades arrive at "
            "irregular times, which estimator is efficient is still open. <bookmark mark='b'/> If volatility is rough, "
            "as Part 14 will argue, its path is nearly as irregular as the price's, and estimating the spot volatility "
            "itself converges very slowly. <bookmark mark='c'/> And telling a jump in the price from a jump in its "
            "volatility, or a jump shared by many assets, with finite data, is an active problem."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a day's 5-minute RV is $4.0 \times 10^{-4}$ and its realized quarticity $\mathrm{RQ}$ is $2.4 \times "
                       r"10^{-7}$. Give a 95\% interval for the integrated variance, and for the day's volatility.")
        with self.voiceover(
            "Pause and predict. A day's five-minute realized variance is four times ten to the minus four, and its "
            "realized quarticity two point four times ten to the minus seven. Give a ninety-five percent interval for "
            "the integrated variance, and for the day's volatility."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
