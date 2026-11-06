from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, ITO, PART, load



class Research(VoiceoverScene):
    def construct(self):
        t = load("rv_theory")
        self.card()
        self.theorem()
        self.proof()
        self.coverage(t)
        self.log_fix(t)
        self.breaks()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The error in realized variance", r"How well can a day's volatility be measured from its "
                          r"prices?", part=PART)
        with self.voiceover(
            'For the researcher: Chapter 2 measured quadratic variation from prices sampled finer and finer. How '
            "well, exactly? The answer is a central limit theorem, with an error bar from a single day's data."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        thm = theorem_card(r"A central limit theorem for realized variance", VGroup(
            MathTex(r"dX_t = \sigma_t\,dW_t,\qquad \mathrm{RV}_n = \textstyle\sum_{i=1}^n (X_{i/n} - X_{(i-1)/n})^2", font_size=30),
            MathTex(r"\sqrt n\,\Big(\mathrm{RV}_n - \textstyle\int_0^1\sigma_s^2\,ds\Big)\ \xrightarrow{\ \text{stably}\ }\ "
                    r"\mathcal{MN}\Big(0,\ 2\textstyle\int_0^1\sigma_s^4\,ds\Big)", font_size=30),
            MathTex(r"\frac{\mathrm{RV}_n - \mathrm{IV}}{\sqrt{2\,\mathrm{RQ}_n/n}} \Rightarrow N(0, 1),\quad \mathrm{RQ}_n = "
                    r"\tfrac n3\textstyle\sum (\Delta_i X)^4", font_size=30, color=ITO),
            wrapped_label((
                              'continuous It\\^o-semimartingale volatility; positive integrated quarticity; localization for '
                              'moments; no jumps or observation noise; an asymptotic limit'
                          ),
                          10.4, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25), who=r"Jacod (1994); Barndorff-Nielsen and Shephard (2002)", width=11.4,
            font_size=24).move_to(UP * 0.2)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> For a continuous Itô price with a continuous, locally bounded "
            'Itô-semimartingale volatility, observed without noise, sample log price n times a day and add up '
            "squared returns. Localize to meet the needed moment conditions. The error against the day's "
            'integrated variance shrinks like one over root n, and tends to a mixed normal: normal given the '
            'volatility path, with a variance of twice the integrated quarticity, the integral of sigma to the '
            "fourth. <bookmark mark='b'/> The quarticity is itself estimated from the fourth powers of the "
            'returns, and the studentized error converges to a standard normal. So a realized variance comes with'
            " a standard error, computed from the same day's data."
        ) as vo:
            self.play(FadeIn(thm), run_time=0.5)
            vo.wait_until("a")
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
            "The proof is Part 5's machinery again. <bookmark mark='a'/> Write the error as a sum over intervals:"
            " each squared return, less the variance that accrued in it. <bookmark mark='b'/> By Itô's isometry "
            "each term has conditional mean zero, so the sum is a martingale. <bookmark mark='c'/> Over a short "
            'interval the return is close to normal, so its square, centred, has variance two sigma to the fourth'
            " over n squared. <bookmark mark='d'/> Add these up, scale by n, and the Riemann sum tends to twice "
            'the integrated quarticity. Freezing volatility on each small interval controls the remainder. '
            'Conditional Lindeberg and asymptotic orthogonality to the original driving martingales give the '
            'stable mixed-normal limit. Consistent quarticity estimation then permits studentization.'
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
        foot = wrapped_label(f"{t['M']} simulated days of 23{{,}}400 one-second steps: 30\\% annual volatility, a U-shaped intraday pattern and a log-normal volatility path; no noise, no jumps. The interval is asymptotic: coarse sampling undercovers; the error decreases with finer sampling", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            'Check it on three thousand simulated days, each with clustering volatility and a U-shaped intraday '
            "pattern. <bookmark mark='a'/> At ten-minute sampling, thirty-nine returns a day, the ninety-five "
            'percent interval covers eighty-nine percent of days: the asymptotics have not quite arrived, and the'
            ' studentized error is a little too wide. At five minutes it covers ninety-two; at one minute '
            'ninety-four; at ten seconds and at one second, ninety-five. And the error itself falls like one over'
            " root n, from twenty-seven percent of the day's variance at ten minutes to about one percent at one "
            'second.'
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def log_fix(self, t):
        rows = [cmath(r"\log\mathrm{RV}_n - \log\mathrm{IV}", r"\approx", r"\frac{\mathrm{RV}_n - \mathrm{IV}}{\mathrm{IV}}",
                      font_size=32, colors={r"\log\mathrm{RV}_n - \log\mathrm{IV}": ITO}),
                cmath(r"z_{\log}", r"=", r"\frac{\log\mathrm{RV}_n - \log\mathrm{IV}}{\sqrt{2\,\mathrm{RQ}_n/(n\,\mathrm{RV}_n^2)}}"
                      r"\ \Rightarrow\ N(0, 1)", font_size=32, colors={r"z_{\log}": ITO})]
        whys = [why(r"the delta method: the log has the same limit, scaled by $1/\mathrm{IV}$"),
                why(r"Barndorff-Nielsen and Shephard (2005): the estimated quarticity moves with $\mathrm{RV}$ itself, which "
                    r"skews the raw statistic; the ratio $\mathrm{RQ}/\mathrm{RV}^2$ is far more stable, so the log "
                    r"statistic is closer to normal in finite samples")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        ns = t["ns"]
        lab = {39: r"10 min", 78: r"5 min", 390: r"1 min", 2340: r"10 s", 23400: r"1 s"}
        hx = [-3.4, -0.4, 2.0, 4.6]
        head = VGroup(label(r"sampling", font_size=18, color=GREY_B), label(r"raw: covers, skew", font_size=18),
                      label(r"log: covers, skew", font_size=18, color=ITO), label(r"", font_size=18))
        tab = VGroup()
        for j_, n in enumerate(ns[:3]):
            c = t["clt"][str(n)]
            row = VGroup(label(lab[n], font_size=18, color=BM),
                         MathTex(rf"{100 * c['cover95']:.1f}\%,\ {c['skew_t']:.2f}", font_size=24),
                         MathTex(rf"{100 * c['cover95_log']:.1f}\%,\ {c['skew_log']:.2f}", font_size=24, color=ITO))
            for i_, cell in enumerate(row):
                cell.move_to([hx[i_], -0.6 - 0.6 * j_, 0])
            row[0].align_to(np.array([hx[0] - 1.6, 0, 0]), LEFT)
            tab.add(row)
        for i_, cell in enumerate(head[:3]):
            cell.move_to([hx[i_], 0.0, 0])
        VGroup(head[:3], tab).move_to(ORIGIN)
        with self.voiceover(
            'At coarse sampling the raw statistic is skewed, and a simple transformation improves it without '
            "guaranteeing finite-sample coverage. <bookmark mark='a'/> Take logs. By the delta method the log of "
            'realized variance has the same limit, scaled by one over the integrated variance. <bookmark '
            "mark='b'/> Studentize it the same way. The raw statistic is skewed because its estimated quarticity "
            'rises and falls with the realized variance itself; in the log version that ratio is far steadier. '
            "<bookmark mark='c'/> On the same simulated days, the log interval covers ninety-two percent at ten "
            'minutes instead of eighty-nine, and the skewness falls from minus one point three to minus point '
            'four.'
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeOut(VGroup(*rows, *whys)), FadeIn(head[:3]),
                      LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def breaks(self):
        cards = VGroup(
            desk_question(r"noise", (
                                        'iid mean-zero observation noise independent of the efficient martingale price adds $2n\\omega^2$ to '
                                        "expected realized variance. Part 7 measures it on Bitcoin's one-minute data and corrects it with "
                                        'two-scale and kernel estimators'
                                    ), width=12.4, font_size=19),
            desk_question(r"jumps", r"realized variance also collects every jump's square; bipower variation removes them, and "
                          r"the gap is a test for jumps (Part 7, chapter 10)", width=12.4, font_size=19),
            desk_question(r"what the theorem guarantees", (
                                                              'for a continuous semimartingale observed without error, an asymptotic error bar under stated '
                                                              'regularity; finite-sample coverage must still be checked'
                                                          ), width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.22)
        self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.5)
        with self.voiceover(
            'The theorem assumes two things real data break, and Part 7 takes both up on real prices. <bookmark '
            "mark='a'/> With independent, identically distributed mean-zero observation noise independent of the "
            'efficient price, expected realized variance gains two n times the noise variance and diverges as '
            "sampling gets finer. <bookmark mark='b'/> And jumps, whose squares it collects on top of the "
            "integrated variance. <bookmark mark='c'/> What the theorem guarantees is the baseline: under the "
            'stated regularity and noise-free assumptions, an asymptotically calibrated error bar from one day’s '
            'data. The coverage experiment shows why that is not a guarantee at coarse frequencies.'
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[k]) if k == 0 else FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: noise that is not white", (
                                                                (
                                                                    'in the standard independent-noise model, the optimal rate is $n^{-1/4}$ (pre-averaging, realized '
                                                                    'kernels, quasi-likelihood); with noise correlated with returns, irregular trading times and price '
                                                                    'discreteness, efficiency depends on the specified noise and observation model; broader combinations '
                                                                    'remain under study'
                                                                )
                                                            ), width=12.4, font_size=18),
            desk_question(r"open: spot volatility when volatility is rough", (
                                                                                 "Part 14's rough volatility can make the variance path rougher than the price; estimating $\\sigma_t$ "
                                                                                 'itself, not its integral, converges very slowly and the right rates are debated'
                                                                             ), width=12.4, font_size=18),
            desk_question(r"open: jumps in volatility, and co-jumps", r"telling a jump in the price from a jump in its "
                          r"volatility, and jumps common to many assets, with finite data", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.5)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With noise the best possible rate is one over n to the "
            'quarter, and several estimators reach it, but when the noise is correlated with returns and trades '
            'arrive at irregular times, efficiency depends on the specified observation and noise model; results '
            "exist for important cases, with broader combinations still under study. <bookmark mark='b'/> If "
            'volatility is rough, as Part 14 will argue, its local paths can be rougher than the price path, and '
            "estimating the spot volatility itself converges very slowly. <bookmark mark='c'/> And telling a jump"
            ' in the price from a jump in its volatility, or a jump shared by many assets, with finite data, is '
            'an active problem.'
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[k]) if k == 0 else FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a 390-minute day's 5-minute RV ($n=78$) is $4.0 \times 10^{-4}$ and its realized quarticity $\mathrm{RQ}$ is $2.4 \times "
                       r"10^{-7}$. Give a 95\% interval for the integrated variance, and for the day's volatility.")
        with self.voiceover(
            "Pause and predict. A day's five-minute realized variance is four times ten to the minus four, and "
            'its realized quarticity two point four times ten to the minus seven. Give a ninety-five percent '
            "interval for the integrated variance, and for the day's volatility."
        ):
            self.play(FadeIn(q))
        self.wait(2)
        answer = VGroup(
            MathTex(r"\widehat{\operatorname{se}} = \sqrt{2\,\mathrm{RQ}/78} = 7.8\times10^{-5}",
                    font_size=32, color=ITO),
            MathTex(r"\mathrm{RV}\pm1.96\widehat{\operatorname{se}}\approx[2.5,\,5.5]\times10^{-4}",
                    font_size=32),
            MathTex((
                        '\\sqrt{\\mathrm{IV}}\\in[1.6\\%,\\,2.4\\%]\\quad(\\text{point estimate }2.0\\%)'
                    ),
                    font_size=32, color=BM),
            wrapped_label(r"an asymptotic interval: the finite-sample coverage experiment still applies", 10.6, 19, GREY_B),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            'Use seventy-eight returns in a three-hundred-and-ninety-minute trading day. The estimated standard '
            'error is seven point eight times ten to the minus five. Add and subtract one point nine six standard'
            ' errors: about two point five to five point five times ten to the minus four. Taking square roots '
            'gives daily volatility from one point six to two point four percent, around the two percent point '
            'estimate. This is an asymptotic interval, with the finite-sample limitations just measured.'
        ):
            self.play(FadeOut(q), FadeIn(answer[0]))
            self.play(LaggedStart(*[FadeIn(row) for row in answer[1:]], lag_ratio=0.4))
        self.clear_scene()
