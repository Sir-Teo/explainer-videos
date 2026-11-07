from __future__ import annotations

import numpy as np

from videos.stats.stats57.common import *  # noqa: F403


class Lemma(VoiceoverScene):
    def construct(self):
        self.card()
        self.exchange()
        self.strip()
        self.proof()
        self.exact()
        self.small_n()
        self.ties()
        self.law()
        self.beta_proof()
        self.pac()
        self.split_rows()

    def card(self):
        card = chapter_card(1, r"Exchangeability and the quantile lemma", r"One fact, \ proved", lit=(2005,), part=PART)
        with self.voiceover("Chapter one. Exchangeability, and the quantile lemma that everything else rests on."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def exchange(self):
        rows = [
            cmath(r"(Z_1, \dots, Z_{n+1})", r"\overset{d}{=}", r"(Z_{\pi(1)}, \dots, Z_{\pi(n+1)}) \ \text{ for every permutation } \pi", font_size=32),
            cmath(r"\text{i.i.d.}", r"\Rightarrow", r"\text{exchangeable; \ not conversely (sampling without replacement)}", font_size=32),
            cmath(r"\text{de Finetti}", r":", r"\text{infinite exchangeable sequences are mixtures of i.i.d. ones}", font_size=32),
            cmath(r"\text{all we assume}", r":", r"\text{the test point is exchangeable with the calibration points}", font_size=32),
        ]
        rows[3][-1].set_color(TESTPT)
        whys = [why(r"the definition"), why(r"weaker than independence"), why(r"Part 43"), why(r"nothing about $P$")]
        head = label('Exchange', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Exchangeability: the joint law of the n plus one data points is unchanged by any "
            "permutation. <bookmark mark='b'/> Independent and identically distributed data are exchangeable, but so is sampling "
            "without replacement from a finite population, which is not independent. <bookmark mark='c'/> De Finetti's theorem, "
            "from Part forty-three, says infinite exchangeable sequences are exactly mixtures of i.i.d. ones. <bookmark "
            "mark='d'/> And that is all distribution-free prediction assumes: the test point is exchangeable with the "
            "calibration points. Nothing about the distribution itself."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def strip(self):
        n, alpha = 19, 0.1
        rs = RankStrip(n, alpha, width=12.0).move_to([0, 0.4, 0])
        r = np.random.default_rng(57).integers(1, n + 2, size=12)
        dots = [rs.drop(int(k)) for k in r]
        head = label(r"this part's instrument: \ the rank strip", font_size=28, color=GREY_A).to_edge(UP, buff=0.7)
        foot = fit_rows(VGroup(
            label(rf"$n = {n}$ calibration scores and one test score: \ {n + 1} possible ranks, \ each equally likely", font_size=24, color=GREY_A),
            label(rf"green: \ ranks $1$ to $\lceil (n+1)(1-\alpha)\rceil = {rs.k}$: \ covered", font_size=24, color=COVC),
            label(rf"red: \ the top {n + 1 - rs.k} ranks: \ missed", font_size=24, color=MISSC),
            label(rf"coverage $= {rs.k}/{n + 1} = {rs.k / (n + 1):.2f}$, \ whatever the distribution", font_size=26, color=TESTPT),
        ), 12.4, 0.3, [0, -1.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> This part's instrument is the rank strip. With nineteen calibration scores and one test score, there are twenty possible ranks for the test score, and, assuming almost surely distinct scores, exchangeability makes each rank equally likely. <bookmark mark='b'/> If the threshold is the eighteenth smallest calibration score, the test point is covered whenever its rank is eighteen or less: the green slots. <bookmark mark='c'/> It is missed in the top two: the red. <bookmark mark='d'/> Drop test points at random, and they land uniformly. The coverage is exactly eighteen twentieths, ninety percent, whatever their distribution, provided there are no ties; randomization or conservative ranks handle ties."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rs.slots), FadeIn(rs.lab_lo), FadeIn(rs.lab_hi))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[rs.slots[i].animate.set_fill(COVC, opacity=0.35) for i in range(rs.k)], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d_, shift=DOWN * 0.4) for d_ in dots], lag_ratio=0.25), FadeIn(foot[3]), run_time=4.0)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"S_i = s(Z_i)", r":", r"\text{scores, \ } i \le n + 1: \ \text{exchangeable}", font_size=36),
            cmath(r"P\big(\mathrm{rank}_{\min}(S_{n+1}) \le k\big)", r"\ge", r"\frac{k}{n+1} \ \ \text{(equality without ties)}", font_size=34),
            cmath(r"\hat q", r"=", r"S_{(k)} \text{ among } S_1, \dots, S_n, \ \ k = \lceil (n+1)(1 - \alpha)\rceil", font_size=34),
            cmath(r"S_{n+1} \le \hat q", r"\iff", r"\mathrm{rank}_{\min}(S_{n+1}) \le k \ \Rightarrow \ P \ge \frac{\lceil (n+1)(1-\alpha)\rceil}{n+1} \ge 1 - \alpha \qquad \blacksquare", font_size=30),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"any fixed score, \ fit on separate data"), why(r"uniform ranks"), why(r"the empirical quantile, \ inflated"), why(r"the quantile lemma")]
        head = label('The guarantee and its assumptions', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The proof in four lines. Apply any fixed score function, say the absolute residual of a model fitted on separate data, to each point: the scores are exchangeable too. <bookmark mark='b'/> Use the minimal rank, one plus the number of scores strictly smaller. Its probability of being at most k is at least k over n plus one. With almost surely distinct scores the rank is uniform and equality holds. <bookmark mark='c'/> Take the threshold to be the k-th smallest calibration score, with k the ceiling of n plus one times one minus alpha, or infinity if k exceeds n. <bookmark mark='d'/> The test score is below the threshold exactly when its rank is at most k, so the coverage is at least that ceiling over n plus one, which is at least one minus alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def exact(self):
        d = load("lemma")
        rows = d["rows"]
        hdr = [r"$n$", r"$k$", r"exact coverage $k/(n+1)$", r"upper bound $1 - \alpha + \frac{1}{n+1}$"]
        body = [[f"{r['n']}", f"{r['k']}", f"{r['exact']:.4f}", f"{min(1.0, r['upper']):.4f}"] for r in rows]
        tab = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.22, colors=[GREY_B] + [WHITE] * len(body)).move_to([0, 0.3, 0])
        foot = label(r"$\alpha = 0.1$: \ never below 90\%, \ never above $90\% + 1/(n + 1)$", font_size=26, color=COVC).move_to([0, -3.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Without ties the coverage is exactly k over n plus one, so the guarantee is also an upper "
            "bound: it never exceeds one minus alpha plus one over n plus one. <bookmark mark='b'/> With four calibration "
            "points it is a hundred percent, because no finite threshold is small enough; with ten, ninety point nine; with a "
            "hundred and one, ninety point two; with two hundred and fifty, ninety point zero four. Conformal prediction is "
            "neither conservative nor anticonservative: it is exact, up to one over n."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def small_n(self):
        rows = [
            cmath(r"n = 19, \ \alpha = 0.1", r":", r"k = \lceil 20 \times 0.9 \rceil = 18: \ \text{coverage } 18/20 = 90\%", font_size=34),
            cmath(r"n = 20", r":", r"k = \lceil 18.9 \rceil = 19: \ \text{coverage } 19/21 = 90.5\%", font_size=34),
            cmath(r"n = 8", r":", r"k = \lceil 8.1 \rceil = 9 > n: \ \text{the whole line}", font_size=36),
            cmath(r"\text{in general}", r":", r"\text{finite only if } n \ge (1 - \alpha)/\alpha = 9", font_size=36),
        ]
        rows[0][-1].set_color(COVC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"exact"), why(r"a little over"), why(r"too few to say"), why(r"the price of no model")]
        head = label('Small n', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Some worked numbers. With nineteen calibration scores and alpha a tenth, k is the "
            "ceiling of twenty times point nine, eighteen: the eighteenth smallest score is the threshold, and the "
            "coverage is eighteen in twenty, exactly ninety percent. <bookmark mark='b'/> With twenty scores, k is "
            "nineteen and the coverage nineteen in twenty-one, ninety and a half percent: a little over. <bookmark "
            "mark='c'/> With only eight scores, k would be nine, more than there are, and the interval is the whole "
            "line. <bookmark mark='d'/> In general a finite interval at level one minus alpha needs at least one minus "
            "alpha over alpha calibration points: nine at ninety percent, ninety-nine at ninety-nine percent."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ties(self):
        rows = [
            cmath(r"\text{ties}", r":", r"\text{discrete scores: \ coverage} \ge \text{, \ not } =, \ k/(n+1)", font_size=36),
            cmath(r"\text{randomize}", r":", r"\text{break ties with } U \sim \mathrm{Unif}(0, 1): \ \text{exact again}", font_size=34),
            cmath(r"\text{smoothed } p\text{-value}", r"=", r"\frac{\#\{S_i > S\} + U(1 + \#\{S_i = S\})}{n + 1}", font_size=34),
            cmath(r"\text{exactly}", r":", r"\mathrm{Unif}(0, 1) \text{ under exchangeability}", font_size=36),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"classification scores"), why(r"Part 46's randomized tests"), why(r"Part 34's function"), why(r"exact, \ any law")]
        head = label('Ties', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> With discrete scores, such as classification probabilities, ties make the coverage "
            "at least k over n plus one rather than equal to it. <bookmark mark='b'/> Breaking ties with an "
            "independent uniform variable restores exactness, just as Part forty-six's randomized tests did. <bookmark "
            "mark='c'/> The smoothed conformal p-value counts the calibration scores above the test score, plus a "
            "uniform fraction of the ties. <bookmark mark='d'/> Under exchangeability it is exactly uniform, whatever "
            "the distribution."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def law(self):
        d = load("lemma")
        c = np.asarray(d["cond"])
        bins = np.linspace(0.78, 1.0, 23)
        h, _ = np.histogram(c, bins)
        A = axes([0.78, 1.0], [0, max(h) * 1.15], x_length=7.4, y_length=4.4, xlabel=r"$P(Y \in C \mid$ this calibration set$)$", ylabel=r"calibration sets",
                 xticks=[0.8, 0.85, 0.9, 0.95, 1.0], yticks=[0, 200, 400], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(b1, 0)[0] - ax.c2p(b0, 0)[0] - 0.03, height=max(ax.c2p(0, k)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                  fill_color=CALC, fill_opacity=0.8).move_to([(ax.c2p(b0, 0)[0] + ax.c2p(b1, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, k)[1]) / 2, 0])
                        for b0, b1, k in zip(bins[:-1], bins[1:], h)])
        L = d["law"]
        xs = np.linspace(0.78, 1.0, 200)
        dens = stats_beta_pdf(xs, L["a"], L["b"]) * len(c) * (bins[1] - bins[0])
        curve = polyline(ax, xs, dens, WHITE, 3)
        side = fit_rows(VGroup(
            label(rf"4,000 calibration sets of $n = {d['n']}$", font_size=22),
            label(rf"each gives one interval; \ its coverage of future points", font_size=22, color=CALC),
            label(rf"white: \ Beta$({L['a']}, {L['b']})$, \ exactly \ (Vovk 2012)", font_size=22, color=WHITE),
            label(rf"mean {d['mean']:.3f}; \ {100 * d['below85']:.1f}\% of sets below 85\%", font_size=22, color=MISSC),
            label(r"larger $n$ concentrates it: \ variance $\approx \alpha(1-\alpha)/n$", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The guarantee is on average over the calibration set too. Draw four thousand calibration sets of a hundred. <bookmark mark='b'/> Each gives one interval, and that interval has some coverage of future points. <bookmark mark='c'/> With independent identically distributed continuous scores, conditional on separately trained models, that coverage has a Beta distribution, with parameters k and n plus one minus k. <bookmark mark='d'/> Its mean is {say(d['mean'], 3)}, but {100 * d['below85']:.1f} percent of calibration sets give intervals that cover less than eighty-five percent. <bookmark mark='e'/> A larger calibration set concentrates it, with variance about alpha times one minus alpha over n: choose n with that in mind."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ Beta law exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(curve), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def beta_proof(self):
        rows = [
            cmath(r"\text{given the calibration set}", r":", r"\text{coverage} = F(\hat q) = F(S_{(k)})", font_size=34),
            cmath(r"F(S_{(1)}), \dots, F(S_{(n)})", r":", r"\text{the order statistics of } n \text{ uniforms}", font_size=34),
            cmath(r"U_{(k)}", r"\sim", r"\mathrm{Beta}(k, n + 1 - k), \ \ \text{mean } \tfrac{k}{n+1}, \ \text{variance} \approx \tfrac{\alpha(1-\alpha)}{n}", font_size=32),
            cmath(r"\text{PAC}", r":", r"\text{choose } k \text{ so that } P(\text{coverage} \ge 1 - \alpha) \ge 1 - \delta", font_size=34),
        ]
        rows[2][-1].set_color(COVC)
        rows[3][-1].set_color(CALC)
        whys = [why(r"IID continuous scores; \ fixed separately trained model"), why(r"the probability integral transform"), why(r"Wilks's fact"), why(r"training-conditional guarantees")]
        head = label('Beta proof', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The Beta law is Wilks's fact for independent identically distributed continuous scores. Mere exchangeability is not enough for the Beta law. Given the calibration set, the interval's coverage of a future point is the score distribution F evaluated at the threshold, the k-th order statistic. <bookmark mark='b'/> F of the scores are n independent uniforms, so F of the k-th score is the k-th uniform order statistic, <bookmark mark='c'/> which is Beta with parameters k and n plus one minus k: mean k over n plus one, variance about alpha times one minus alpha over n. <bookmark mark='d'/> That gives a stronger guarantee with a width cost: choose k a little larger, and with probability one minus delta over the calibration set, the coverage itself is at least one minus alpha. Vovk calls this training-conditional validity."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pac(self):
        rows = [
            cmath(r"n = 100, \ \alpha = 0.1", r":", r"k = 91: \ \mathrm{Beta}(91, 10), \ \text{mean } 90.1\%, \ \text{SD } 3.0", font_size=34),
            cmath(r"\text{its 5\% quantile}", r":", r"84.8\%: \ \text{one deployment in 20 below it}", font_size=36),
            cmath(r"\text{PAC choice}", r":", r"k = 96: \ P(\text{coverage} \ge 90\%) \ge 0.95", font_size=36),
            cmath(r"\text{the cost}", r":", r"\text{the 96th of 100 scores, \ not the 91st: \ wider}", font_size=36),
        ]
        rows[1][-1].set_color(MISSC)
        rows[2][-1].set_color(COVC)
        whys = [why(r"chapter 1's numbers"), why(r"from the Beta law"), why(r"Vovk's calibration-conditional rule"), why(r"a stricter threshold")]
        head = label('Pac', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> With a hundred calibration points at alpha a tenth, k is ninety-one and the "
            "coverage, given the calibration set, is Beta with parameters ninety-one and ten: mean ninety point one "
            "percent, standard deviation three points. <bookmark mark='b'/> Its five percent quantile is eighty-four "
            "point eight percent: one deployment in twenty gets a calibration set that leaves it below that. <bookmark "
            "mark='c'/> To guarantee ninety percent coverage with probability ninety-five percent over the calibration "
            "set, take k equal to ninety-six instead. <bookmark mark='d'/> The cost is a wider interval: the "
            "ninety-sixth of a hundred scores, not the ninety-first."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def split_rows(self):
        rows = [
            cmath(r"\text{split conformal}", r":", r"\text{fit } \hat\mu \text{ on one half; \ scores } |Y_i - \hat\mu(X_i)| \text{ on the other}", font_size=32),
            cmath(r"C(x)", r"=", r"[\hat\mu(x) - \hat q, \ \hat\mu(x) + \hat q]: \ \ P(Y_{n+1} \in C(X_{n+1})) \ge 1 - \alpha", font_size=32),
            cmath(r"\text{any } \hat\mu", r":", r"\text{a bad model gives wide intervals, \ preserves marginal validity under exchangeability}", font_size=34),
            cmath(r"\text{better scores}", r":", r"\text{CQR, \ normalized residuals \ (Part 34): \ adaptive width}", font_size=32),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"Papadopoulos et al.; \ Lei et al. (2018)"), why(r"the lemma, \ applied"), why(r"validity is free"), why(r"efficiency is not")]
        head = label('Split rows', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Split conformal prediction is the lemma applied. Fit any model on one part of the data, and compute absolute residuals on the other. <bookmark mark='b'/> The interval is the prediction plus or minus their inflated quantile, and it covers a new point with probability at least one minus alpha. <bookmark mark='c'/> Any separately trained model preserves marginal validity under the required exchangeability. A bad score can hurt width and subgroup coverage. <bookmark mark='d'/> Validity is free; efficiency is not, and comes from better scores, such as conformalized quantile regression or residuals divided by a fitted spread."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()


def stats_beta_pdf(x, a, b):
    from scipy import stats

    return stats.beta.pdf(x, a, b)
