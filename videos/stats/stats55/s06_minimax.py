from __future__ import annotations

import math

import numpy as np

from videos.stats.stats55.common import *  # noqa: F403


class ExamMinimax(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p9()
        self.p10()

    def card(self):
        card = chapter_card(5, r"Sitting V: \ minimax and high-dimensional probability", r"Problems 9 and 10", lit=(1994, 2012), part=PART)
        with self.voiceover("Sitting five: minimax theory and high-dimensional probability. Fano's inequality for sparse means, and matrix Bernstein."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 9
    def p9(self):
        d = load("fano")
        card = ExamCard(9, r"a Fano lower bound for sparse estimation", r"Part 50", [
            r"$Y = \theta + \sigma Z/\sqrt n$ in $\mathbb R^d$, \ $\theta$ with at most $s \le d/8$ nonzero entries.",
            r"With a sparse Varshamov--Gilbert packing and Fano's inequality, \ prove",
            r"$\inf_{\hat\theta}\sup_\theta E\|\hat\theta - \theta\|^2 \ge c\,\sigma^2 s\log(1 + d/2s)/n$. \ Which estimator attains the rate?"],
            marks=10, color=HDC)
        self.pose_voiceover(
            "Problem nine. Observe a d-dimensional mean with Gaussian noise of variance sigma squared over n, where the mean "
            "has at most s nonzero entries. Using a packing of sparse binary vectors and Fano's inequality, prove that no "
            "estimator has worst-case squared error below a constant times sigma squared s log of one plus d over two s, "
            "over n. Which estimator attains the rate? Pause and try it.", card)
        rows = [
            cmath(r"\omega_1, \dots, \omega_M \in \{0, 1\}^d", r":", r"|\omega_j| = s, \ \ \rho(\omega_j, \omega_k) \ge s/2, \ \ \log M \ge \tfrac s8\log(1 + \tfrac{d}{2s})", font_size=30),
            cmath(r"\theta_j = \delta\,\omega_j", r":", r"\|\theta_j - \theta_k\|^2 \ge s\delta^2/2, \ \ \mathrm{KL}(P_j, P_k) = \tfrac{n}{2\sigma^2}\|\theta_j - \theta_k\|^2 \le \tfrac{n s\delta^2}{\sigma^2}", font_size=30),
            cmath(r"\text{Fano}", r":", r"\text{risk} \ge \frac{s\delta^2}{8}\Big(1 - \frac{n s\delta^2/\sigma^2 + \log 2}{\log M}\Big)", font_size=32),
            cmath(r"\delta^2 = \frac{\sigma^2(\log M - \log 2)}{2ns}", r":", r"\text{risk} \ge \frac{\sigma^2(\log M - \log 2)^2}{32\, n\log M} \asymp \frac{\sigma^2 s\log(d/s)}{n}", font_size=30),
        ]
        rows[0][-1].set_color(HDC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"Rigollet \& H\"utter, \ Lemma 4.14"), why(r"far apart, \ hard to tell apart"), why(r"Part 50"), why(r"optimize $\delta$")]
        self.steps_voiceover("<bookmark mark='a'/> The packing: there are M binary vectors with exactly s ones, any two differing in at "
                   "least s over two places, with log M at least s over eight times log of one plus d over two s. <bookmark "
                   "mark='b'/> Scale them by delta. Any two are at squared distance at least s delta squared over two, while "
                   "the Kullback–Leibler divergence between their data distributions, n over two sigma squared times the "
                   "squared distance, is at most n s delta squared over sigma squared. <bookmark mark='c'/> Fano's inequality "
                   "from Part fifty: the minimax risk is at least a quarter of the squared separation, times one minus the "
                   "divergence plus log two, over log M. <bookmark mark='d'/> Choose delta to balance the two, and the bound "
                   "becomes sigma squared times log M minus log two squared, over thirty-two n log M: of order sigma squared s "
                   "log of d over s, over n.", rows, whys)
        self.clear_but(card)
        self.p9_table(d, card)
        self.p9_upper(card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. A packing of sparse vectors, <bookmark mark='b'/> separated in "
                       "squared distance but close in Kullback–Leibler divergence, <bookmark mark='c'/> Fano's inequality, "
                       "<bookmark mark='d'/> and an estimator from Part thirty-two that attains the rate from above.", [(r"a sparse packing", 50), (r"separation vs KL", 50), (r"Fano's inequality", 50),
                        (r"soft thresholding: \ upper", 32)], "abcd", color=HDC)

    def p9_upper(self, card):
        rows = [
            cmath(r"\hat\theta_i = \eta_\lambda(Y_i)", r"=", r"\mathrm{sign}(Y_i)(|Y_i| - \lambda)_+, \ \ \lambda = \sigma\sqrt{2\log d/n}", font_size=32),
            cmath(r"E\|\hat\theta - \theta\|^2", r"\le", r"(2\log d + 1)\Big(\frac{\sigma^2}{n} + \sum_i \min\big(\theta_i^2, \frac{\sigma^2}{n}\big)\Big)", font_size=32),
            cmath(r"\theta \ s\text{-sparse}", r"\Rightarrow", r"E\|\hat\theta - \theta\|^2 \le (2\log d + 1)(s + 1)\,\sigma^2/n", font_size=34),
            cmath(r"\text{so}", r":", r"\text{the bounds meet: \ the minimax rate}", font_size=34),
        ]
        rows[1][-1].set_color(HDC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"soft thresholding"), why(r"Donoho \& Johnstone (1994)"), why(r"each coordinate: \ signal or noise"), why(r"$s\log(d/s)$ with a refined $\lambda$")]
        self.steps_voiceover(
            "<bookmark mark='a'/> The upper bound, to finish the problem. Soft thresholding at sigma root two log d "
            "over n shrinks every coordinate toward zero and kills the small ones. <bookmark mark='b'/> Donoho and "
            "Johnstone's oracle inequality bounds its risk by two log d plus one, times the noise level plus the sum "
            "over coordinates of the smaller of the squared signal and the noise level: what an oracle choosing to "
            "keep or kill each coordinate would pay, times a logarithm. <bookmark mark='c'/> For an s-sparse vector "
            "that is at most two log d plus one, times s plus one, times sigma squared over n. <bookmark mark='d'/> So "
            "Fano's lower bound and thresholding's upper bound meet, up to constants, and with the threshold tuned to "
            "log of d over s instead of log d, the rate is exactly sigma squared s log of d over s, over n.",
            rows, whys)
        self.clear_but(card)

    def p9_table(self, d, card):
        s, n = d["s"], d["n"]
        rows_ = [r for r in d["rows"] if r["d"] in (100, 1000, 10000, 100000)]
        hdr = [r"$d$", r"rate $\frac{s\log(ed/s)}{n}$", r"$\frac{2s\log(d/s)}{n}$", r"soft thresh., worst", r"Fano bound"]
        body = [[f"{r['d']:,}", f"{r['rate']:.3f}", f"{2 * s * math.log(r['d'] / s) / n:.3f}", f"{r['soft']:.3f}", f"{r['lower']:.5f}"] for r in rows_]
        tab = table_rows([hdr] + body, font_size=22, col_buff=0.5, row_buff=0.2,
                         colors=[GREY_B] + [WHITE] * len(body)).move_to([0, -0.4, 0])
        foot = fit_rows(VGroup(
            label(rf"$s = {s}$, \ $n = {n}$, \ $\sigma = 1$; \ soft thresholding at $\sqrt{{2\log(d/s)/n}}$, \ the worst of four signal sizes", font_size=22, color=GREY_A),
            label(r"all grow like $\log d$; \ Fano's constant is poor, \ the rate is right", font_size=24, color=PROOFC),
            label(r"the exact constant: \ $2\sigma^2 s\log(d/s)/n$ \ (Donoho \& Johnstone 1994)", font_size=22, color=HDC),
        ), 12.4, 0.25, [0, -2.85, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The numbers, with ten nonzero entries and a hundred observations, as the dimension grows "
            f"from a hundred to a hundred thousand. <bookmark mark='b'/> Soft thresholding at the universal threshold, in its "
            f"worst case over four signal sizes, has risk growing like log d, about twice the rate s log e d over s, over n. "
            f"<bookmark mark='c'/> Fano's bound grows like log d too, but its constant is poor, hundreds of times smaller: "
            f"minimax lower bounds are about rates. <bookmark mark='d'/> The exact asymptotic constant, two sigma squared s "
            f"log d over s, over n, is attained by thresholding, as David Donoho and Iain Johnstone showed in 1994."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(exact_tag(r"bounds exact; \ thresholding simulated")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r[3] for r in tab[1:]]), color=HDC))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_but(card)

    # ------------------------------------------------------------------------------------------ Problem 10
    def p10(self):
        d = load("bernstein")
        r4 = [r for r in d["rows"] if r["n"] == 400][0]
        card = ExamCard(10, r"matrix Bernstein for a covariance", r"Part 51", [
            r"$x_1, \dots, x_n \in \mathbb R^d$ i.i.d.\ with independent $\pm 1$ coordinates, \ so $E xx^\top = I$ and $\|x\|^2 = d$.",
            r"Use matrix Bernstein to bound $E\|\hat\Sigma - I\|$ \ ($\hat\Sigma = \frac1n\sum x_i x_i^\top$, \ operator norm),",
            r"and give a 95\% confidence ball for $\Sigma$. \ Compare with simulation and with Marchenko--Pastur."],
            marks=10, color=HDC)
        self.pose_voiceover(
            "Problem ten. Independent vectors in d dimensions whose coordinates are independent random signs, so their "
            "covariance is the identity and their squared length is exactly d. Use the matrix Bernstein inequality to bound "
            "the expected operator-norm error of the sample covariance, and turn the tail bound into a ninety-five percent "
            "confidence ball for the covariance matrix. Compare with simulation and with the Marchenko–Pastur edge. Pause "
            "and try it.", card)
        rows = [
            cmath(r"\hat\Sigma - I", r"=", r"\textstyle\sum_i Z_i, \ \ Z_i = \frac1n(x_i x_i^\top - I): \ \text{independent, \ mean } 0, \ \|Z_i\| \le \frac dn = L", font_size=30),
            cmath(r"(xx^\top)^2 = d\,xx^\top", r"\Rightarrow", r"\textstyle\sum_i E Z_i^2 = \frac{1}{n}(d - 1) I: \ \ v = \frac{d - 1}{n}", font_size=32),
            cmath(r"P\big(\|\textstyle\sum Z_i\| \ge t\big)", r"\le", r"2d\exp\Big(-\frac{t^2/2}{v + Lt/3}\Big), \ \ E\|\cdot\| \le \sqrt{2v\log 2d} + \frac{L\log 2d}{3}", font_size=30),
            cmath(r"\text{ball}", r":", r"t_\delta = \tfrac{Lc}{3} + \sqrt{(\tfrac{Lc}{3})^2 + 2vc}, \ \ c = \log(2d/\delta): \ P(\|\hat\Sigma - \Sigma\| \le t_\delta) \ge 1 - \delta", font_size=28),
        ]
        rows[2][-1].set_color(HDC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"a sum of random matrices"), why(r"the matrix variance"), why(r"Tropp (2012)"), why(r"solve the quadratic in $t$")]
        self.steps_voiceover("<bookmark mark='a'/> Write the error as a sum of independent, mean-zero random matrices, each the rank-one "
                   "deviation divided by n, with operator norm at most d over n. <bookmark mark='b'/> Because x x transpose "
                   "squared is d times x x transpose, the matrix variance is d minus one over n times the identity. <bookmark "
                   "mark='c'/> Matrix Bernstein, in Joel Tropp's form, bounds the tail by two d times a Bernstein exponent, and "
                   "integrating gives the expected norm: the root of two v log two d, plus L log two d over three. <bookmark "
                   "mark='d'/> Setting the tail bound to delta and solving the quadratic in t gives the radius of a confidence "
                   "ball that holds with probability at least ninety-five percent, for every n.", rows, whys)
        self.clear_but(card)
        self.p10_chart(d, card)
        self.p10_log(card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        br = load("board")["rows"]
        show_board(self, board_rows("Bernstein"),
                   f"<bookmark mark='a'/> On the Board, two thousand samples of four hundred: the matrix-Bernstein ball, of "
                   f"radius {say(r4['t'], 2)}, contains the true covariance every time, {100 * br[3]['achieved']:.0f} percent. "
                   f"Conservative by design: a dimension-free argument pays for its generality.", [("a", [0])])
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Write the error as a sum, <bookmark mark='b'/> compute its "
                       "matrix variance, <bookmark mark='c'/> apply matrix Bernstein, whose proof rests on Lieb's concavity "
                       "theorem for the trace exponential, <bookmark mark='d'/> and invert the tail bound into a confidence "
                       "set, Part forty-six's old move.", [(r"a sum of random matrices", 51), (r"the matrix variance $v$", 51), (r"Lieb's trace inequality", 51),
                        (r"a ball, \ for every $n$", 46)], "abcd", color=HDC)

    def p10_log(self, card):
        rows = [
            cmath(r"\text{a } \tfrac14\text{-net}", r":", r"9^d \text{ points, \ a union bound}: \ \|\hat\Sigma - I\| \lesssim \sqrt{d/n}", font_size=34),
            cmath(r"\text{matrix Bernstein}", r":", r"\text{no net, \ but the factor } 2d \text{ in front: \ } \sqrt{d\log d/n}", font_size=32),
            cmath(r"\log d \text{ needed?}", r":", r"\text{not here; \ for random diagonal sums, \ yes}", font_size=34),
            cmath(r"\text{the trade}", r":", r"\text{a norm and a variance suffice; \ the price is } \sqrt{\log d}", font_size=34),
        ]
        rows[1][-1].set_color(HDC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"Part 51's $\varepsilon$-nets, \ for sub-Gaussian vectors"), why(r"Tropp's dimensional factor"), why(r"coupon-collector sums"), why(r"universality has a price")]
        self.steps_voiceover(
            "<bookmark mark='a'/> Why the logarithm? Part fifty-one had a second route: cover the sphere with a net of "
            "at most nine to the d points, bound each quadratic form by a scalar Bernstein inequality, and take a "
            "union bound. For sub-Gaussian vectors like these, that gives the root of d over n, with no logarithm. "
            "<bookmark mark='b'/> Matrix Bernstein needs no net, but carries a factor of two d in front of the "
            "exponential, which costs a root log d. <bookmark mark='c'/> For these vectors the logarithm is not "
            "needed, as the Marchenko–Pastur edge showed. For sums of random diagonal matrices, where a few "
            "coordinates collect most of the mass by chance, as in the coupon collector's problem, it is. <bookmark "
            "mark='d'/> Matrix Bernstein needs only a bound on each summand's norm and the matrix variance, and that "
            "generality is what the logarithm buys.",
            rows, whys)
        self.clear_but(card)

    def p10_chart(self, d, card):
        ns = np.log10([r["n"] for r in d["rows"]])
        A = axes([1.95, 3.85], [-0.9, 0.7], x_length=6.8, y_length=3.4, xlabel=rf"$n$ \ (log scale), \ $d = {d['d']}$", ylabel=r"$\log_{10}\|\hat\Sigma - I\|$",
                 xticks=[2, 3, np.log10(6400)], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-0.5, 0, 0.5], center=CHART)
        ax = A.ax

        def line_(key, col, dash=False):
            c = polyline(ax, ns, np.log10([r[key] for r in d["rows"]]), col, 4)
            return DashedVMobject(c, num_dashes=30) if dash else c

        cm = line_("mean", S.EST)
        cq = line_("q95", S.ALT)
        cb = line_("mean_bound", HDC, dash=True)
        ct = line_("t", PROOFC, dash=True)
        cmp_ = line_("mp", WHITE, dash=True)
        r4 = [r for r in d["rows"] if r["n"] == 400][0]
        side = fit_rows(VGroup(
            label(rf"$n = 400$: \ blue: \ simulated mean {r4['mean']:.2f}; \ teal: \ 95th percentile {r4['q95']:.2f}", font_size=22, color=S.EST),
            label(rf"dashed white: \ the Marchenko--Pastur edge, \ {r4['mp']:.2f}", font_size=22, color=WHITE),
            label(rf"dashed red: \ the Bernstein mean bound, \ {r4['mean_bound']:.2f}", font_size=22, color=HDC),
            label(rf"dashed green: \ the ball's radius, \ {r4['t']:.2f}", font_size=22, color=PROOFC),
            label(r"all fall like $\sqrt{d\log d/n}$ or better", font_size=22, color=GREY_A),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The error against n, with fifty dimensions. In blue, its simulated mean: {say(r4['mean'], 2)} "
            f"at four hundred observations; in teal, its ninety-fifth percentile, {say(r4['q95'], 2)}. <bookmark mark='b'/> "
            f"The Marchenko–Pastur edge of Part fifty-two, one plus the root of d over n, squared, minus one, predicts them "
            f"almost exactly: {say(r4['mp'], 2)}. <bookmark mark='c'/> The matrix Bernstein bound on the mean is "
            f"{say(r4['mean_bound'], 2)}, <bookmark mark='d'/> and the ball's radius {say(r4['t'], 2)}: about twice the truth, "
            f"for an argument that knows nothing about this distribution beyond its norm and variance. <bookmark mark='e'/> "
            f"All of them fall at the same rate, up to the logarithm that the matrix argument pays."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bounds exact")))
            vo.wait_until("a")
            self.play(Create(cm), Create(cq), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cmp_), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cb), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ct), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)
