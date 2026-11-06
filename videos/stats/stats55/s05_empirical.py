from __future__ import annotations

import numpy as np

from videos.stats.stats55.common import *  # noqa: F403


class ExamEmpirical(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p7()
        self.p8()

    def card(self):
        card = chapter_card(4, r"Sitting IV: \ empirical processes and efficiency", r"Problems 7 and 8", lit=(1952, 1974, 1882), part=PART)
        with self.voiceover("Sitting four: empirical processes and efficiency. A bracketing bound, and an influence function on Newcomb's data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 7
    def p7(self):
        d = load("brackets")
        card = ExamCard(7, r"a bracketing bound for a Donsker class", r"Part 48", [
            r"$\mathcal F = \{x \mapsto 1\{x \le t\}: t \in \mathbb R\}$, \ $P$ a continuous law on $\mathbb R$.",
            r"Show $N_{[\,]}(\varepsilon, \mathcal F, L_2(P)) \le \lceil 1/\varepsilon^2 \rceil$, \ that the bracketing integral is finite,",
            r"and conclude that $\mathcal F$ is $P$-Donsker. \ Which smoothness classes fail the same test?"], marks=10, color=EMPC)
        self.pose_voiceover(
            "Problem seven. Take the class of indicators of half-lines, one of x at most t, and a continuous distribution on "
            "the line. Show that the number of L two brackets of size epsilon needed to cover the class is at most the "
            "ceiling of one over epsilon squared, that the bracketing entropy integral is finite, and conclude that the class "
            "is Donsker. Then say which smoothness classes fail the same test. Pause and try it.", card)
        rows = [
            cmath(r"-\infty = t_0 < \dots < t_m = \infty", r":", r"P(t_{j-1} < X \le t_j) \le \varepsilon^2, \ \ m = \lceil 1/\varepsilon^2 \rceil", font_size=32),
            cmath(r"\|u_j - \ell_j\|_{L_2(P)}", r"=", r"P(t_{j-1} < X \le t_j)^{1/2} \le \varepsilon", font_size=34),
            cmath(r"J_{[\,]}", r"=", rf"\int_0^1 \sqrt{{\log N_{{[\,]}}(\varepsilon)}}\,d\varepsilon \le \int_0^1 \sqrt{{\log(2/\varepsilon^2)}}\,d\varepsilon < \infty \ \ ({d['integral']:.2f})", font_size=30),
            cmath(r"\text{Ossiander}", r":", r"J_{[\,]} < \infty \Rightarrow \sqrt n(F_n - F) \rightsquigarrow \mathbb B \circ F \ \ (\text{Donsker 1952})", font_size=32),
        ]
        rows[2][-1].set_color(EMPC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"quantiles of $P$, \ by continuity"), why(r"$[\ell_j, u_j] = [1\{x \le t_{j-1}\}, 1\{x \le t_j\}]$"), why(r"numerically, \ the ceiling included"), why(r"the bracketing CLT (Part 48)")]
        self.steps_voiceover("<bookmark mark='a'/> Cut the line at quantiles of P, so that each piece has probability at most epsilon "
                   "squared; by continuity that takes the ceiling of one over epsilon squared pieces. <bookmark mark='b'/> The "
                   "bracket for the j-th piece runs from the indicator of x at most t j minus one to the indicator of x at most "
                   "t j. Their difference is the indicator of the piece, whose L two norm is the root of its probability, at "
                   "most epsilon, and every half-line indicator lies in one of the brackets. <bookmark mark='c'/> So the "
                   f"bracketing entropy is about two log one over epsilon, whose square root is integrable at zero: the "
                   f"integral is about {say(d['integral'], 2)}. <bookmark mark='d'/> Ossiander's bracketing central limit "
                   f"theorem from Part forty-eight then says the class is Donsker: the empirical process converges to a "
                   f"Brownian bridge composed with F, which is Donsker's theorem of 1952.", rows, whys)
        self.clear_but(card)
        self.p7_chart(d, card)
        rows = [
            cmath(r"\text{monotone } [0,1] \to [0,1]", r":", r"\log N_{[\,]} \asymp 1/\varepsilon: \ \int \varepsilon^{-1/2} < \infty, \ \text{Donsker}", font_size=32),
            cmath(r"\text{H\"older-}\alpha \text{ on } [0,1]^d", r":", r"\log N_{[\,]} \asymp \varepsilon^{-d/\alpha}: \ \text{integrable iff } \alpha > d/2", font_size=32),
            cmath(r"\text{Lipschitz on } [0,1]^2", r":", r"\int \varepsilon^{-1}\,d\varepsilon = \infty: \ \text{the test fails}", font_size=32),
            cmath(r"\text{the moral}", r":", r"\text{smoothness must beat dimension, \ the curse of Part 50}", font_size=32),
        ]
        rows[1][-1].set_color(EMPC)
        rows[2][-1].set_color(S.RESID)
        whys = [why(r"van de Geer; \ Birman--Solomjak"), why(r"Kolmogorov--Tikhomirov (1959)"), why(r"$d/\alpha = 2$"), why(r"rates slow, \ then the CLT fails")]
        self.steps_voiceover("<bookmark mark='a'/> Other classes. Monotone functions from the unit interval to itself have bracketing "
                   "entropy of order one over epsilon: its square root is still integrable, so they are Donsker too. "
                   "<bookmark mark='b'/> Hölder-smooth functions of order alpha on the d-dimensional cube have entropy of order "
                   "epsilon to the minus d over alpha, by Kolmogorov and Tikhomirov, and the integral is finite exactly when "
                   "alpha exceeds d over two. <bookmark mark='c'/> Lipschitz functions on the square sit right on the "
                   "boundary, where the integral diverges, and the bracketing test fails. <bookmark mark='d'/> Smoothness must "
                   "beat dimension: the same curse that slows the minimax rates of Part fifty.", rows, whys)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Cut at quantiles, <bookmark mark='b'/> build brackets of "
                       "size epsilon, <bookmark mark='c'/> integrate the root of the entropy, the same integral as Dudley's "
                       "chaining in Part fifty-one, <bookmark mark='d'/> and apply the bracketing central limit theorem.", [(r"cut at quantiles", 48), (r"brackets of size $\varepsilon$", 48), (r"the entropy integral", 51),
                        (r"Ossiander: \ Donsker", 48)], "abcd", color=EMPC)

    def p7_chart(self, d, card):
        grid = np.asarray(d["grid"])
        proc = np.asarray(d["proc"])
        br = np.asarray(d["brackets"])
        A = axes([0, 1], [-1.0, 1.0], x_length=6.8, y_length=3.4, xlabel=r"$t$ \ ($P$ uniform)", ylabel=r"$\sqrt n\,(F_n(t) - t)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-1, 0, 1], center=CHART)
        ax = A.ax
        bands = VGroup(*[Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, 1.0)[1] - ax.c2p(0, -1.0)[1],
                                   stroke_width=0, fill_color=EMPC, fill_opacity=0.10 if k % 2 == 0 else 0.22)
                         .move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
                         for k, (a, b) in enumerate(zip(br[:-1], br[1:]))])
        path = polyline(ax, grid, proc, S.EST, 3)
        side = fit_rows(VGroup(
            label(rf"purple bands: \ the {len(br) - 1} brackets for $\varepsilon = 1/4$", font_size=22, color=EMPC),
            label(rf"blue: \ the empirical process, \ $n = {d['n']}$", font_size=22, color=S.EST),
            label(rf"its supremum: \ {d['sup']:.2f} \ (Kolmogorov's median: \ 0.83)", font_size=22, color=GREY_A),
            label(r"finitely many brackets at every scale: \ tight, \ so it converges", font_size=22, color=PROOFC),
        ), 4.6, 0.4, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The picture for the uniform distribution. The purple bands are the sixteen brackets for "
            f"epsilon one quarter: each has probability one sixteenth, so each bracket's width in L two is a quarter. "
            f"<bookmark mark='b'/> In blue, one empirical process, root n times F n minus F, for four hundred draws. "
            f"<bookmark mark='c'/> Its largest excursion is {say(d['sup'], 2)}; Kolmogorov's limit law has median about "
            f"zero point eight three. <bookmark mark='d'/> Within each bracket the process can move only a little, and there "
            f"are finitely many brackets at every scale: that is the tightness that makes the whole process converge."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"one simulated sample")))
            vo.wait_until("a")
            self.play(FadeIn(bands), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(path), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_but(card)

    # ------------------------------------------------------------------------------------------ Problem 8
    def p8(self):
        d = load("median")
        card = ExamCard(8, r"the median's influence function", r"Part 49", [
            r"$m(P) = F^{-1}(1/2)$, \ with $F$ having a density $f > 0$ at $m$. \ Derive the efficient influence function",
            r"of $m$ in the nonparametric model, \ and its variance. \ Apply it to Newcomb's 66 passage times",
            r"(with two outliers): \ the median, \ a Wald interval, \ and the mean's, \ compared."], marks=10, color=EMPC)
        self.pose_voiceover(
            "Problem eight. The median of a distribution with a positive density at the median. Derive its efficient influence "
            "function in the nonparametric model, and its variance. Then apply it to Simon Newcomb's sixty-six measurements of "
            "the time light takes to cross the Potomac and back, which include two outliers: give the median, a Wald interval, "
            "and compare them with the mean's. Pause and try it.", card)
        rows = [
            cmath(r"\text{a path } P_t", r":", r"dP_t = (1 + t g)\,dP, \ \ E g = 0: \ \ F_t(m_t) = \tfrac12 \text{ for all } t", font_size=32),
            cmath(r"\tfrac{d}{dt}\big|_0", r":", r"E\big[1\{X \le m\} g(X)\big] + f(m)\, \dot m = 0", font_size=34),
            cmath(r"\dot m", r"=", r"E\Big[\frac{\tfrac12 - 1\{X \le m\}}{f(m)}\, g(X)\Big]: \ \ \tilde\psi(x) = \frac{\tfrac12 - 1\{x \le m\}}{f(m)}", font_size=32),
            cmath(r"\mathrm{Var}\,\tilde\psi", r"=", r"\frac{1}{4 f(m)^2}: \ \ \text{normal } \pi/2 = 1.571, \ \ t_3: \ 1.851 \ (\text{vs } 3 \text{ for the mean})", font_size=30),
        ]
        rows[2][-1].set_color(EMPC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"a one-dimensional submodel"), why(r"differentiate the defining equation"), why(r"subtract $\frac12 E g = 0$: \ the gradient"), why(r"the nonparametric tangent space is everything")]
        self.steps_voiceover("<bookmark mark='a'/> Take any smooth path through P, with score g of mean zero, and let m t be the median "
                   "along it, so F t of m t is a half for every t. <bookmark mark='b'/> Differentiate at zero: the derivative of "
                   "F t at the fixed point m is the expectation of the indicator times g, and the chain rule adds f of m times "
                   "the derivative of the median. <bookmark mark='c'/> Solving, and subtracting a half times the mean of g, "
                   "which is zero, writes the derivative as an inner product with g: the gradient is one half minus the "
                   "indicator, over f of m. In the nonparametric model the tangent space is everything, so this gradient is "
                   "the efficient influence function. <bookmark mark='d'/> Its variance is one over four f of m squared: pi "
                   "over two for the normal, worse than the mean's one, but one point eight five for a t with three degrees of "
                   "freedom, much better than the mean's three.", rows, whys)
        self.clear_but(card)
        self.p8_if(d, card)
        self.p8_newcomb(d, card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        br = load("board")["rows"]
        show_board(self, board_rows("median"),
                   f"<bookmark mark='a'/> On the Board, four thousand samples of sixty-six from a t with three degrees of "
                   f"freedom, heavy-tailed like Newcomb's: the median plus or minus 1.96 influence-function standard errors, "
                   f"with a kernel estimate of the density, covers {100 * br[2]['achieved']:.1f} percent of the time. "
                   f"Conservative, because the kernel smooths the peak and underestimates f, which widens the interval.",
                   [("a", [0])])
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. A path through the model, <bookmark mark='b'/> the defining "
                       "equation differentiated, <bookmark mark='c'/> the gradient read off as an inner product, and <bookmark "
                       "mark='d'/> its variance, which is Part thirty's robustness seen through Part forty-nine's efficiency "
                       "theory.", [(r"a smooth path, \ score $g$", 49), (r"differentiate $F_t(m_t) = \frac12$", 49),
                        (r"the gradient: \ bounded", 49), (r"variance $1/4f^2$; \ Newcomb", 30)], "abcd", color=EMPC)

    def p8_if(self, d, card):
        g = np.asarray(d["grid"])
        A = axes([-3, 3], [-3, 3], x_length=6.8, y_length=3.4, xlabel=r"$x$ \ ($P = N(0, 1)$)", ylabel=r"influence $\tilde\psi(x)$",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-2, 0, 2], center=CHART)
        ax = A.ax
        cm = polyline(ax, g, d["if_mean"], S.EST, 4)
        left = Line(ax.c2p(-3, d["if_normal"][0]), ax.c2p(0, d["if_normal"][0]), color=EMPC, stroke_width=5)
        right = Line(ax.c2p(0, d["if_normal"][-1]), ax.c2p(3, d["if_normal"][-1]), color=EMPC, stroke_width=5)
        side = fit_rows(VGroup(
            label(r"blue: \ the mean's, \ $x - \mu$: \ unbounded", font_size=22, color=S.EST),
            label(rf"purple: \ the median's, \ $\pm 1/(2f(0)) = \pm{abs(d['if_normal'][0]):.3f}$", font_size=22, color=EMPC),
            label(r"one wild point moves the mean without limit", font_size=22, color=S.RESID),
            label(r"and moves the median by at most $1/(2nf)$", font_size=22, color=PROOFC),
        ), 4.6, 0.4, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The two influence functions at the standard normal. The mean's is the straight line x "
            f"minus mu: unbounded. <bookmark mark='b'/> The median's is a step, plus or minus one over two f of zero, "
            f"{say(abs(d['if_normal'][0]), 3)}. <bookmark mark='c'/> A single wild observation can move the mean as far as it "
            f"likes, <bookmark mark='d'/> but it moves the median by at most about one over two n f, wherever it lands."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(Create(cm), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(left), Create(right), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_but(card)

    def p8_newcomb(self, d, card):
        x = np.sort(np.asarray(d["x"]))
        A = axes([-48, 42], [0, 3], x_length=6.8, y_length=3.0, xlabel=r"passage time $-$ 24{,}800 ns", ylabel=r"",
                 xticks=[-40, -20, 0, 20, 40], yticks=[], center=[-2.6, -1.25, 0])
        ax = A.ax
        # a dot plot: stack repeated values
        dots, seen = VGroup(), {}
        for v in x:
            k = seen.get(v, 0)
            seen[v] = k + 1
            dots.add(Dot(ax.c2p(v, 0.18 + 0.16 * k), radius=0.05, color=DATA))
        med = d["median"]
        ci, cm_ = d["ci"], d["ci_mean"]
        mbar = VGroup(Line(ax.c2p(ci[0], 2.2), ax.c2p(ci[1], 2.2), color=EMPC, stroke_width=6), Dot(ax.c2p(med, 2.2), radius=0.08, color=EMPC))
        abar = VGroup(Line(ax.c2p(cm_[0], 2.7), ax.c2p(cm_[1], 2.7), color=S.EST, stroke_width=6), Dot(ax.c2p(d["mean"], 2.7), radius=0.08, color=S.EST))
        truth = DashedLine(ax.c2p(d["modern"], 0), ax.c2p(d["modern"], 3), color=WHITE, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"Newcomb, \ 1882: \ {d['n']} passage times; \ outliers {d['outliers'][0]:.0f} and {d['outliers'][1]:.0f}", font_size=22, color=DATA),
            label(rf"purple: \ median {med:.1f}, \ $\hat f = {d['f']:.3f}$, \ SE {d['se']:.2f}: \ ({ci[0]:.1f}, {ci[1]:.1f})", font_size=22, color=EMPC),
            label(rf"blue: \ mean {d['mean']:.2f}, \ SE {d['se_mean']:.2f}: \ ({cm_[0]:.1f}, {cm_[1]:.1f})", font_size=22, color=S.EST),
            label(rf"without the outliers the mean is {d['clean_mean']:.2f}", font_size=22, color=GREY_A),
            label(rf"white: \ the modern value, \ {d['modern']:.0f}: \ neither covers it", font_size=22, color=WHITE),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> Newcomb's sixty-six passage times, in nanoseconds above twenty-four thousand eight hundred, "
            f"with the two outliers, minus forty-four and minus two, far to the left. <bookmark mark='b'/> The median is "
            f"{say(med, 0)}. A kernel estimate of the density there is {say(d['f'], 3)}, so the influence-function standard "
            f"error is {say(d['se'], 2)}, and the Wald interval runs from {say(ci[0], 1)} to {say(ci[1], 1)}. <bookmark "
            f"mark='c'/> The mean, {say(d['mean'], 2)}, is dragged left by the outliers, and its standard error is "
            f"{say(d['se_mean'], 2)}, nearly twice the median's. <bookmark mark='d'/> Without the two outliers the mean would "
            f"be {say(d['clean_mean'], 2)}. <bookmark mark='e'/> And the modern value of the speed of light corresponds to "
            f"thirty-three: neither interval covers it. Every interval in this course measures random error only; Newcomb's "
            f"apparatus had a systematic one."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Newcomb (1891); \ Stigler (1977)")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.02), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(mbar), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(abar), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(truth), FadeIn(side[4]))
        self.clear_but(card)
