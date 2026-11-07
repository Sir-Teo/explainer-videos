from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class CramerRao(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.statement()
        self.proof()
        self.geometry()
        self.attainment()
        self.exponential()
        self.tanks()
        self.biased()

    def card(self):
        card = chapter_card(10, r"The Cram\'er--Rao bound", r"How good can an unbiased estimator possibly be?", lit=(1946,), part=PART)
        with self.voiceover("Chapter ten. The Cramér–Rao bound."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        h1 = history_card(1945, r"C. R. Rao, \ Calcutta", r"the bound, \ with information as its measure of accuracy", color=LIK,
                          width=4.0, font_size=22).move_to([-4.3, 0.9, 0])
        h2 = history_card(1946, r"Harald Cram\'er, \ Stockholm", r"\emph{Mathematical Methods of Statistics}, \ written in wartime "
                          r"Sweden: \ the bound, \ and the theory of ch.~5 made rigorous", color=LIK, width=4.0, font_size=22).move_to([0, 0.9, 0])
        h3 = history_card(1943, r"Maurice Fr\'echet, \ Paris", r"the same inequality, \ earlier; \ and Aitken \& Silverstone (1942), \ "
                          r"Darmois (1945)", color=GREY_B, width=4.0, font_size=22).move_to([4.3, 0.9, 0])
        foot = label(r"some call it the information inequality, \ to share the credit", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        intro = label('The information inequality had several discoverers', font_size=36)
        with self.voiceover(
            "This result was found several times in a few years. <bookmark mark='a'/> Rao proved it in the same 1945 "
            "paper as the Rao–Blackwell theorem. <bookmark mark='b'/> Harald Cramér proved it in his 1946 book, "
            "Mathematical Methods of Statistics, written in neutral Sweden during the war, which also made the "
            "large-sample theory of chapter five rigorous and trained a generation of statisticians. "
            "<bookmark mark='c'/> Maurice Fréchet had it in 1943, Georges Darmois in 1945, and Alexander Aitken and "
            "Harold Silverstone came close in 1942. <bookmark mark='d'/> So some books call it the information "
            "inequality, which shares the credit."
        ) as vo:
            self.play(FadeIn(intro))
            for k, (m_, h) in enumerate(zip("abc", (h1, h2, h3))):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(h, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def statement(self):
        tc = theorem_card(r"The Cram\'er--Rao bound", r"Under the regularity conditions, \ if $T$ is unbiased for $\psi(\theta)$ from $n$ "
                          r"i.i.d.\ observations, \ then \ $\displaystyle \mathrm{Var}_\theta\,T \;\ge\; \frac{\psi'(\theta)^2}{n\,I(\theta)}$ \ "
                          r"for every $\theta$.", who=r"Rao (1945); \ Cram\'er (1946)", color=LIK, width=10.4, font_size=28).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\psi(\theta) = \theta:\qquad \mathrm{SD}(T) \;\ge\; \frac{1}{\sqrt{n\,I(\theta)}}", font_size=34, color=S.ACCENT),
            label(r"a speed limit: \ no unbiased estimator's error can shrink faster than $1/\sqrt n$", font_size=26),
        ), 12.6, 0.4, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The statement. Under the regularity conditions, any unbiased estimator of a function "
            "psi of theta, from n independent observations, has variance at least psi prime squared over n times the "
            "information. <bookmark mark='b'/> For theta itself, the standard deviation is at least one over root n I. "
            "<bookmark mark='c'/> It's a speed limit. However clever the recipe, if it's unbiased, its error can't "
            "shrink faster than one over root n, and the constant is fixed by the information. And chapter five said "
            "the MLE achieves this limit in large samples: maximum likelihood is asymptotically as good as any unbiased "
            "estimator can be. That's what Fisher had claimed in 1922."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\psi(\theta)", r"=", r"E_\theta T = \int T(x)\,p_\theta(x)\,dx", font_size=34),
            cmath(r"\psi'(\theta)", r"=", r"\int T(x)\,U_\theta(x)\,p_\theta(x)\,dx = \mathrm{Cov}_\theta(T, U)", font_size=34),
            cmath(r"\psi'(\theta)^2", r"\le", r"\mathrm{Var}_\theta T\cdot\mathrm{Var}_\theta U", font_size=34),
            cmath(r"\vphantom{x}", r"=", r"\mathrm{Var}_\theta T\cdot n\,I(\theta)", font_size=34),
            cmath(r"\mathrm{Var}_\theta T", r"\ge", r"\frac{\psi'(\theta)^2}{n\,I(\theta)}", font_size=36),
        ]
        rows[4][2].set_color(LIK)
        whys = [why(r"unbiased, \ for every $\theta$"), why(r"differentiate under the integral; \ $E U = 0$ makes it a covariance"),
                why(r"Cauchy--Schwarz: \ a correlation is at most 1"), why(r"the score of $n$ observations has variance $nI$ (ch.~9)"),
                why(r"divide: \ done")]
        intro = label('Unbiasedness and Cauchy--Schwarz imply a bound', font_size=36)
        with self.voiceover(
            "The proof is four lines, and the key is Cauchy–Schwarz. <bookmark mark='a'/> Unbiasedness says the mean "
            "of T is psi of theta, for every theta. <bookmark mark='b'/> So we can differentiate it in theta. The "
            "derivative of the density is the score times the density, and since the score has mean zero, the result is "
            "the covariance between T and the score. <bookmark mark='c'/> A covariance squared is at most the product "
            "of the variances, the Cauchy–Schwarz inequality: a correlation can't exceed one. "
            "<bookmark mark='d'/> The score's variance is n times the information. <bookmark mark='e'/> Divide, and "
            "that's the bound. Every unbiased estimator must be correlated with the score, because its mean has to "
            "track theta; and its correlation with the score can't exceed one, so its variance can't be too small."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=5, top=2.9, x=-0.6, buff=0.5, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def geometry(self):
        o = np.array([-2.2, -1.4, 0])
        U = Arrow(o, o + np.array([4.6, 0, 0]), buff=0, color=LIK, stroke_width=6)
        ang = 0.85
        Tlen = 3.4
        tip = o + Tlen * np.array([np.cos(ang), np.sin(ang), 0])
        T = Arrow(o, tip, buff=0, color=UMVUE, stroke_width=6)
        proj = np.array([tip[0], o[1], 0])
        drop = DashedLine(tip, proj, color=GREY_B, stroke_width=2)
        pseg = Line(o, proj, color=S.ACCENT, stroke_width=9)
        lu = MathTex(r"U\ (\text{the score})", font_size=30, color=LIK).next_to(U.get_end(), DOWN, buff=0.2)
        lt = MathTex(r"T - \psi(\theta)", font_size=30, color=UMVUE).next_to(T.get_end(), UP, buff=0.15)
        lp = MathTex(r"\text{length fixed: } \frac{\mathrm{Cov}(T, U)}{\|U\|} = \frac{|\psi'|}{\sqrt{nI}}", font_size=28,
                     color=S.ACCENT).next_to(pseg, DOWN, buff=0.35)
        arc = Arc(radius=0.7, start_angle=0, angle=ang, arc_center=o, color=GREY_A)
        rows = fit_rows(VGroup(
            label(r"random variables as vectors: \ $\langle X, Y\rangle = \mathrm{Cov}(X, Y)$", font_size=24),
            label(r"unbiasedness fixes $T$'s shadow on the score", font_size=24, color=S.ACCENT),
            label(r"a vector is never shorter than its shadow: \ $\mathrm{SD}(T) \ge |\psi'|/\sqrt{nI}$", font_size=24),
            label(r"equality: \ $T - \psi$ points along $U$, \ $T = \psi + a(\theta)\,U$", font_size=24, color=UMVUE),
        ), 5.2, 0.34, [4.3, 1.6, 0])
        intro = label('The score fixes the projection of an unbiased estimator', font_size=36)
        with self.voiceover(
            "Here's the same proof as a picture. <bookmark mark='a'/> Treat random variables with mean zero as vectors, "
            "with the covariance as the dot product, so a standard deviation is a length. The score is one vector. "
            "<bookmark mark='b'/> T minus its mean is another. <bookmark mark='c'/> Unbiasedness pins down the "
            "covariance of T with the score, so it fixes the length of T's shadow on the score direction. "
            "<bookmark mark='d'/> A vector is never shorter than its shadow. So T's standard deviation is at least the "
            "shadow's length: that's the bound. <bookmark mark='e'/> And it's attained only when T points exactly along "
            "the score, with no sideways component, when T is a linear function of the score."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(GrowArrow(U), FadeIn(lu), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(T), FadeIn(lt), Create(arc))
            vo.wait_until("c")
            self.play(Create(drop), Create(pseg), FadeIn(lp), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            new_tip = o + np.array([proj[0] - o[0], 0.0, 0])
            self.play(T.animate.put_start_and_end_on(o, new_tip + UP * 0.001), lt.animate.next_to(new_tip, UP, buff=0.3),
                      FadeOut(drop), FadeOut(arc), FadeIn(rows[3]))
        self.clear_scene()

    def attainment(self):
        rows = [
            cmath(r"T - \psi(\theta)", r"=", r"a(\theta)\,U_\theta(x)", font_size=34),
            cmath(r"\frac{\partial}{\partial\theta}\log p_\theta(x)", r"=", r"\frac{T(x) - \psi(\theta)}{a(\theta)}", font_size=34),
            cmath(r"\log p_\theta(x)", r"=", r"\eta(\theta)\,T(x) - A(\theta) + \log h(x)", font_size=34),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"equality in Cauchy--Schwarz"), why(r"rearrange"), why(r"integrate in $\theta$: \ an exponential family")]
        foot = fit_rows(VGroup(
            label(r"the bound is attained only by $T$ in an exponential family, \ estimating its mean $\psi = E\,T$", font_size=26,
                  color=S.ACCENT),
            label(r"attained: \ $\bar x$ for a normal $\mu$; \ $\bar x$ for Poisson $\lambda$; \ $x/n$ for $p$", font_size=24),
            label(r"not attained: \ the exponential's rate $\lambda$, \ the normal's $\sigma$, \ $e^{-\lambda}$ \ (UMVUEs still exist)",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.0, 0])
        intro = label('Equality in the information inequality', font_size=36)
        with self.voiceover(
            "When can the bound be reached exactly? <bookmark mark='a'/> Only when T minus its mean is a multiple of "
            "the score, for every theta. <bookmark mark='b'/> Rearranged, the derivative of the log-density is a "
            "function of theta times T, plus another function of theta. <bookmark mark='c'/> Integrate, and the "
            "log-density has exponential-family form, with T as its sufficient statistic. "
            "<bookmark mark='d'/> So the bound is attained only by the natural statistic of an exponential family, "
            "estimating its own mean. <bookmark mark='e'/> The sample mean for a normal mean, or a Poisson rate, or a "
            "proportion. <bookmark mark='f'/> For these other examples, the exponential's rate, a normal standard deviation, "
            "the probability of a quiet year, the best unbiased estimator exists, but its variance sits strictly "
            "above the bound."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.5, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            for k, m_ in enumerate("def"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def exponential(self):
        d = load("cramerrao")
        ns = np.asarray(d["ns"], float)
        lam = d["lam"]
        r_mle = np.asarray(d["mle"]) / np.asarray(d["bound"])
        r_unb = np.asarray(d["unb"]) / np.asarray(d["bound"])
        mse_mle = (np.asarray(d["mle"]) + np.asarray(d["mle_bias"]) ** 2) / np.asarray(d["bound"])
        A = axes([0, 100], [0, 3.2], x_length=6.6, y_length=4.4, xlabel=r"$n$", ylabel=r"variance $\div$ the bound $\lambda^2/n$",
                 xticks=[5, 20, 50, 100], yticks=[0, 1, 2, 3], center=[-2.9, -0.3, 0])
        ax = A.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(100, 1), color=EXACT, stroke_width=2.5)
        xs = np.linspace(3.2, 100, 200)
        ex = curve(ax, xs, xs / (xs - 2), UMVUE, 2.5)
        dots_u = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=UMVUE) for a, b in zip(ns, r_unb)])
        dots_m = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=MAX) for a, b in zip(ns, mse_mle)])
        leg = legend([(EXACT, r"the Cram\'er--Rao bound"), (UMVUE, r"$(n - 1)/S$: \ UMVUE, \ $\tfrac{n}{n - 2}\times$ bound"),
                      (MAX, r"$n/S$: \ the MLE's MSE")], font_size=22).move_to([4.2, 2.0, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"n = 5:\ \ {r_unb[0]:.2f},\ \ {mse_mle[0]:.2f}", font_size=28),
            MathTex(rf"n = 100:\ \ {r_unb[-1]:.2f},\ \ {mse_mle[-1]:.2f}", font_size=28),
            label(r"above the bound at every $n$, \ but the gap closes like $2/n$", font_size=24, color=S.ACCENT),
        ), 4.6, 0.3, [4.2, -1.2, 0])
        tag = simulated_tag(r"simulated: \ 40,000 samples per $n$, \ $\lambda = 0.5$", corner=DR)
        with self.voiceover(
            "The exponential rate shows what that looks like. <bookmark mark='a'/> The bound is lambda squared over n; "
            "divide every variance by it, so the bound becomes the green line at one. <bookmark mark='b'/> The best "
            "unbiased estimator, n minus one over the total, has variance exactly n over n minus two times the bound. "
            "At five observations that's one and two thirds; at a hundred, one point zero two. It never touches the "
            "line, but it approaches it. <bookmark mark='c'/> The MLE, n over the total, is biased, so compare its mean "
            "squared error instead: worse still at small n, nearly three times the bound at n equals five, and also "
            "converging to one. The bound is valid at every sample size under its assumptions, but it need not be tight. Here the unbiased estimator approaches it as the sample grows."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(one), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(ex), FadeIn(dots_u), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots_m), FadeIn(leg[2]), FadeIn(rows))
        self.clear_scene()

    def tanks(self):
        d = load("tanks")
        ks = np.asarray(d["ks"], float)
        lk = np.log10(ks)
        A = axes([0.3, 1.31], [1.0, 2.2], x_length=6.4, y_length=4.6, xlabel=r"tanks captured $k$ (log scale)",
                 ylabel=r"SD, \ $N = 300$ (log scale)", xticks=[np.log10(2), np.log10(5), 1.0, np.log10(20)],
                 yticks=[1.0, np.log10(20), np.log10(50), 2.0], xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{10 ** v:.0f}",
                 center=[-2.9, -0.3, 0])
        ax = A.ax
        mom = polyline(ax, lk, np.log10(d["mom_sd_theory"]), MOM, 3.5)
        umv = polyline(ax, lk, np.log10(d["umvue_sd_theory"]), UMVUE, 3.5)
        # a regular-model "speed limit" with the same value at k = 2: SD proportional to 1/sqrt(k)
        c = d["umvue_sd_theory"][0] * np.sqrt(2)
        lim = DashedVMobject(polyline(ax, lk, np.log10(c / np.sqrt(ks)), WHITE, 2.5), num_dashes=40)
        leg = legend([(MOM, r"$2\bar x - 1$: \ slope $-\tfrac12$"), (UMVUE, r"$m(1 + \tfrac1k) - 1$: \ slope $-1$"),
                      (WHITE, r"any $1/\sqrt k$ rate")], font_size=22).move_to([4.4, 2.1, 0])
        rows = fit_rows(VGroup(
            label(r"the support $\{1, \dots, N\}$ moves with $N$:", font_size=24),
            label(r"integer $N$, moving support: the smooth bound does not apply", font_size=24),
            MathTex(r"\mathrm{Var}\,\hat N_{\mathrm{UMVUE}} = \frac{(N - k)(N + 1)}{k(k + 2)} \approx \frac{N^2}{k^2}\quad(1\ll k\ll N)", font_size=28,
                    color=UMVUE),
            label(r"irregular models can be estimated faster than $1/\sqrt n$", font_size=26, color=S.ACCENT),
            label(r"each new tank moves the edge we are looking for", font_size=22, color=GREY_A),
        ), 4.6, 0.32, [4.3, -0.9, 0])
        with self.voiceover(
            "And now the tanks break the speed limit. <bookmark mark='a'/> On log scales, a one over root k rate is a "
            "line of slope minus a half. The moment estimator approximately follows it while k is small relative to N. <bookmark mark='b'/> For one much smaller than k and k much smaller than N, the best unbiased "
            "estimator approximately falls with slope minus one: its standard deviation shrinks like one over k, not one over root k. "
            "<bookmark mark='c'/> The dashed line is any estimator obeying a one over root k law, matched at two tanks. "
            "By twenty tanks the scaled maximum is already more than twice as accurate, and the gap keeps widening. "
            "<bookmark mark='d'/> How is that allowed? The bound's proof differentiated the density in theta, and here "
            "the set of possible serials, one to N, moves with N. N is integer-valued and the support moves, so the usual score-based Cramér–Rao proof does not apply. Other bounds for irregular models still exist. <bookmark mark='e'/> Each extra captured tank tells us about the edge of the distribution "
            "directly, and the edge is the parameter. Irregular problems, like boundaries and change points, can be "
            "estimated at rate one over n, and Part 47 studies such rates in general."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(mom), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(umv), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(lim), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[:3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def biased(self):
        rows = [
            cmath(r"E_\theta T = \theta + b(\theta)", r"\ \Rightarrow\ ", r"\mathrm{Var}_\theta T \ge \frac{\big(1 + b'(\theta)\big)^2}{n\,I(\theta)}",
                  font_size=32),
            cmath(r"\mathrm{MSE}", r"\ge", r"\frac{\big(1 + b'(\theta)\big)^2}{n\,I(\theta)} + b(\theta)^2", font_size=32),
        ]
        whys = [why(r"the same proof, \ with $\psi(\theta) = \theta + b(\theta)$"), why(r"shrinkage ($-2 < b' < 0$) lowers the variance floor")]
        foot = fit_rows(VGroup(
            label(r"a biased estimator can go below $1/(nI)$, \ at some $\theta$: \ Part 8's $n + 1$ divisor, \ James--Stein", font_size=24),
            label(r"Hodges (1951): \ an estimator that beats the bound at one point, \ asymptotically; \ Le Cam: \ only on a set of "
                  r"measure zero (Part 47)", font_size=24, color=GREY_A),
            label(r"the bound is a benchmark for regular, unbiased estimation, \ not a law of nature", font_size=26, color=S.ACCENT),
        ), 12.6, 0.3, [0, -2.45, 0])
        intro = label('Bias changes the information bound', font_size=36)
        with self.voiceover(
            "Two more ways around the bound. <bookmark mark='a'/> The same proof works for a biased estimator, with "
            "the derivative of its mean in place of one. <bookmark mark='b'/> If the bias shrinks estimates toward a "
            "point, so that the derivative of its mean lies between zero and one, the variance floor drops below one over n I. "
            "<bookmark mark='c'/> So biased estimators can beat the bound at some values of theta: Part 8's n plus one "
            "divisor did, and James–Stein shrinkage does. <bookmark mark='d'/> And in 1951 Joseph Hodges built an "
            "estimator that beats the bound asymptotically at one point, at no cost elsewhere in the limit. Lucien "
            "Le Cam later showed that this can only happen on a negligible set of parameter values, and that such "
            "estimators pay heavily nearby: Part 47 tells that story. <bookmark mark='e'/> The Cramér–Rao bound is a "
            "benchmark for regular, unbiased estimation, not a law of nature."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.9, x=-0.6, buff=0.5, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k], shift=RIGHT * 0.2))
        self.clear_scene()
