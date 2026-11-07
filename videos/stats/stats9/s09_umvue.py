from __future__ import annotations

from math import comb

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


UMV = EST_COL["umvue"]  # the class below takes the colour's name


class UMVUE(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.completeness()
        self.lehmann_scheffe()
        self.tank_complete()
        self.gaps()
        self.families()
        self.absurd()

    def card(self):
        card = chapter_card(8, r"The best unbiased estimator", r"When is an improvement the last one?", part=PART)
        with self.voiceover("Chapter eight. The best unbiased estimator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def question(self):
        boxes = VGroup()
        starts = [(r"2\bar X - 1", MOM), (r"2X_1 - 1", S.PRIOR), (r"X_{(1)} + X_{(k)} - 1", S.POST)]
        for j, (t, c) in enumerate(starts):
            b = VGroup(RoundedRectangle(width=3.2, height=0.9, corner_radius=0.12, stroke_color=c, stroke_width=2),
                       MathTex(t, font_size=30, color=c))
            b[1].move_to(b[0])
            b.move_to([-4.2 + 4.2 * j, 1.8, 0])
            boxes.add(b)
        arrows = VGroup(*[Arrow(b.get_bottom(), [0, -0.4, 0], buff=0.15, color=GREY_B, stroke_width=3) for b in boxes])
        tgt = VGroup(RoundedRectangle(width=4.6, height=1.0, corner_radius=0.12, stroke_color=UMV, stroke_width=3),
                     MathTex(r"E(\,\cdot \mid m) = m\big(1 + \tfrac1k\big) - 1", font_size=30, color=UMV))
        tgt[1].move_to(tgt[0])
        tgt.move_to([0, -0.9, 0])
        rows = fit_rows(VGroup(
            label(r"three unbiased starting points, \ one destination", font_size=26, color=S.ACCENT),
            label(r"is that luck? \ could some other unbiased estimator still beat it?", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.6, 0])
        intro = label('Do different unbiased starts reach the same estimator?', font_size=36)
        with self.voiceover(
            "Rao–Blackwell improves an estimator, but it raises a question. <bookmark mark='a'/> What if we'd started "
            "somewhere else? Here are three unbiased estimators of N: twice the mean minus one; twice the first serial "
            "captured, minus one; and the smallest plus the largest, minus one. <bookmark mark='b'/> Condition each on "
            "the maximum. <bookmark mark='c'/> All three arrive at the same place, the scaled maximum. "
            "<bookmark mark='d'/> Is that a coincidence? And might some other unbiased estimator, one we haven't "
            "thought of, still do better? The property that settles both questions is called completeness."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in boxes], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[GrowArrow(a) for a in arrows])
            vo.wait_until("c")
            self.play(FadeIn(tgt, scale=1.1), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def completeness(self):
        dc = definition_card(r"Complete statistic", r"$T$ is \emph{complete} if \ $E_\theta\, g(T) = 0$ for every $\theta$ \ "
                             r"implies $g(T) = 0$ (with probability one).", color=UMV, width=9.6, font_size=28).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"no non-trivial function of $T$ averages to zero under every $\theta$", font_size=26),
            label(r"so $T$'s distributions are rich enough to tell any two functions of $T$ apart", font_size=24, color=GREY_A),
            label(r"if $g_1(T)$ and $g_2(T)$ are both unbiased for $\tau(\theta)$, \ their difference has mean 0 for every $\theta$: \ "
                  r"$g_1 = g_2$", font_size=24, color=S.ACCENT),
        ), 12.6, 0.36, [0, -1.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A statistic T is complete if the only function of T whose average is zero under "
            "every value of theta is the zero function itself. <bookmark mark='b'/> No non-trivial function of T can "
            "be centred at zero everywhere. <bookmark mark='c'/> Intuitively, the family of T's distributions is rich "
            "enough to distinguish any two functions of T. <bookmark mark='d'/> And here's why we care. Suppose two "
            "functions of T are both unbiased for the same quantity. Then their difference averages to zero for every "
            "theta, so by completeness it's zero. A complete statistic has at most one unbiased function for any "
            "target."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lehmann_scheffe(self):
        tc = theorem_card(r"Lehmann--Scheff\'e", r"If $T$ is complete and sufficient, \ and $g(T)$ is unbiased for $\tau(\theta)$, \ "
                          r"then $g(T)$ is the unique \emph{uniformly minimum-variance unbiased estimator} (UMVUE) of $\tau(\theta)$.",
                          who=r"E. Lehmann \& H. Scheff\'e, \ \emph{Sankhy\=a} (1950, 1955)", color=UMV, width=10.4,
                          font_size=26).move_to([0, 2.0, 0])
        rows = [
            cmath(r"\hat\tau \text{ unbiased}", r"\ \Rightarrow\ ", r"E(\hat\tau \mid T) \text{ unbiased, a function of } T", font_size=30),
            cmath(r"E(\hat\tau \mid T)", r"=", r"g(T)", r"\quad\text{by completeness}", font_size=32),
            cmath(r"\mathrm{Var}\,g(T)", r"=", r"\mathrm{Var}\,E(\hat\tau \mid T) \le \mathrm{Var}\,\hat\tau", font_size=32),
        ]
        rows[2][2].set_color(UMV)
        whys = [why(r"Rao--Blackwell, \ for any unbiased start"), why(r"only one unbiased function of $T$ exists"),
                why(r"so $g(T)$ beats every unbiased $\hat\tau$, \ at every $\theta$")]
        with self.voiceover(
            "<bookmark mark='a'/> That gives the Lehmann–Scheffé theorem, from 1950. If T is complete and sufficient, "
            "and some function of T is unbiased, then that function is the best unbiased estimator there is: it has "
            "the smallest variance among all unbiased estimators, uniformly, at every value of theta. That's the "
            "mouthful U-M-V-U-E. <bookmark mark='b'/> The proof is two lines. Take any unbiased estimator and "
            "Rao–Blackwellize it: the result is unbiased and a function of T. <bookmark mark='c'/> By completeness it "
            "must be g of T, the only unbiased function of T. <bookmark mark='d'/> And Rao–Blackwell says its variance "
            "is no bigger than the starting estimator's. Since we could have started anywhere, g of T beats them all. "
            "Every road leads to the same place, and it's the best place."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=3, top=0.5, x=-0.6, buff=0.5, edge=6.9)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tank_complete(self):
        k = 3
        Ns = [3, 4, 5, 6, 7]
        js = [3, 4, 5, 6, 7]
        cells = VGroup()
        for i, N in enumerate(Ns):
            for j, jj in enumerate(js):
                v = comb(jj - 1, k - 1) / comb(N, k) if jj <= N else 0
                t = MathTex(rf"\tfrac{{{comb(jj - 1, k - 1)}}}{{{comb(N, k)}}}" if jj <= N else "0", font_size=26,
                            color=WHITE if jj <= N else GREY_D)
                t.move_to([-4.6 + 1.25 * j, 1.6 - 0.72 * i, 0])
                cells.add(t)
        rlab = VGroup(*[MathTex(rf"N = {N}", font_size=24, color=GREY_A).move_to([-6.2, 1.6 - 0.72 * i, 0]) for i, N in enumerate(Ns)])
        clab = VGroup(*[MathTex(rf"m = {jj}", font_size=24, color=GREY_A).move_to([-4.6 + 1.25 * j, 2.3, 0]) for j, jj in enumerate(js)])
        diag = VGroup(*[SurroundingRectangle(cells[i * 5 + i], color=UMV, buff=0.06) for i in range(5)])
        rows = fit_rows(VGroup(
            MathTex(r"P_N(m = j) = \binom{j - 1}{k - 1}\Big/\binom Nk,\quad j = k, \dots, N", font_size=28),
            MathTex(r"E_N\,g(m) = 0\ \ \forall N", font_size=28),
            label(r"$N = k$: \ only $j = k$ \ $\Rightarrow g(k) = 0$", font_size=24),
            label(r"$N = k + 1$: \ $\Rightarrow g(k + 1) = 0$; \ and so on", font_size=24),
            label(r"a triangular system: \ $m$ is complete", font_size=26, color=UMV),
        ), 5.4, 0.3, [3.9, -0.1, 0])
        with self.voiceover(
            "Is the tank maximum complete? <bookmark mark='a'/> Its distribution is easy to write down: the chance that "
            "the largest of k serials is j is the number of ways to choose the other k minus one below j, over the "
            "total number of ways. Here's the table for k equals three. Each row is a value of N, each column a value "
            "of the maximum. <bookmark mark='b'/> Suppose some function g of m averages to zero for every N. "
            "<bookmark mark='c'/> Take the first row, N equals k: the maximum must equal k, so g of k is zero. "
            "<bookmark mark='d'/> The second row involves g of k, which we know is zero, and g of k plus one, so that's "
            "zero too. And so on down the diagonal: the system is triangular, and every value of g is forced to zero. "
            "<bookmark mark='e'/> The maximum is complete. So by Lehmann–Scheffé, the scaled maximum, unbiased and a "
            "function of m, is the best unbiased estimator of N. No unbiased recipe, however clever, can beat it for "
            "any N."
        ) as vo:
            self.play(FadeIn(rlab), FadeIn(clab))
            vo.wait_until("a")
            self.play(FadeIn(cells, lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(diag[0]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(dg) for dg in diag[1:]], lag_ratio=0.4), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def gaps(self):
        d = load("tanks")
        one = d["one"]
        k, m = len(one), max(one)
        nl = NumberLine(x_range=[0, 300, 50], length=12.0, include_numbers=True, font_size=22, color=GREY_C).move_to([0, 0.6, 0])
        dots = VGroup(*[Dot(nl.n2p(s_), radius=0.09, color=S.ACCENT) for s_ in one])
        labs = VGroup(*[MathTex(str(s_), font_size=22, color=S.ACCENT).next_to(nl.n2p(s_), UP, buff=0.2) for s_ in one])
        labs[-1].shift(RIGHT * 0.22)
        labs[-2].shift(LEFT * 0.22)
        edges = [0] + list(one)
        gaps = VGroup()
        cols = [S.PRIOR, S.POST, S.LIK, S.TREAT, S.CTRL, S.ALT]
        for i in range(k):
            a, b = edges[i], edges[i + 1]
            if b - a > 1:
                gaps.add(Line(nl.n2p(a + 0.5), nl.n2p(b - 0.5), color=cols[i], stroke_width=9).shift(DOWN * 0.0))
            else:
                gaps.add(VectorizedPoint(nl.n2p(a)))
        avg = (m - k) / k
        extra = Line(nl.n2p(m + 0.5), nl.n2p(m + avg), color=UMV, stroke_width=9)
        est = VGroup(Dot(nl.n2p(m + avg), radius=0.1, color=UMV),
                     MathTex(rf"{m + avg:.1f}", font_size=24, color=UMV).next_to(nl.n2p(m + avg), DOWN, buff=0.45))
        tru = VGroup(Triangle(color=EXACT, fill_opacity=1).scale(0.1).rotate(PI).move_to(nl.n2p(300) + UP * 0.25))
        rows = fit_rows(VGroup(
            MathTex(r"\text{the } k \text{ gaps below the serials: } \ " + " + ".join(str(edges[i + 1] - edges[i] - 1) for i in range(k))
                    + rf" = m - k = {m - k}", font_size=28),
            MathTex(rf"\text{{average gap}} = \frac{{m - k}}{{k}} = {avg:.2f}", font_size=30),
            MathTex(rf"\hat N = m + \frac{{m - k}}{{k}} = m\Big(1 + \frac1k\Big) - 1 = {m + avg:.1f}", font_size=32, color=UMV),
            label(r"assume the unseen gap above $m$ is an average gap", font_size=24, color=S.ACCENT),
        ), 12.6, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "There's a lovely way to see what the best estimator does. <bookmark mark='a'/> Here are our six captured "
            "serials on a line. <bookmark mark='b'/> They split the serials below the maximum into six gaps of unseen "
            "tanks: three below the first, then twenty, forty-four, twenty-seven, a hundred and nine, and five. Their "
            "total is m minus k, two hundred and eight. <bookmark mark='c'/> By symmetry, the gap above the maximum, the "
            "one we can't see, has the same distribution as any of the others. So estimate it by the average gap, "
            "thirty-four point seven. <bookmark mark='d'/> Add it on: two hundred and forty-eight point seven, the best "
            "unbiased estimator. 'The maximum plus the average gap' is the easiest way to remember it. "
            "The truth, three hundred, was further out this time: the unseen gap happened to be big."
        ) as vo:
            self.play(Create(nl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.2), FadeIn(labs))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(gp) for gp in gaps], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(extra), FadeIn(est), FadeIn(rows[2:]))
            self.play(FadeIn(tru))
        self.clear_scene()

    def families(self):
        tc = theorem_card(r"Exponential families are complete",
                          r"if $p_\theta(x) = h(x)\exp\big(\eta(\theta)^\top T(x) - A(\theta)\big)$ \ and the natural parameters "
                          r"$\eta(\theta)$ fill an open set, \ then $T$ is complete and sufficient", who=r"Lehmann \& Scheff\'e (1955); \ Part 45",
                          color=UMV, width=10.4, font_size=26).move_to([0, 2.0, 0])
        items = [
            (r"normal mean, $\sigma$ known", r"\bar x", r"\mu"),
            (r"normal, \ both unknown", r"s^2 = \tfrac{1}{n-1}\sum (x_i - \bar x)^2", r"\sigma^2"),
            (r"Poisson", r"(1 - \tfrac1n)^{S}", r"e^{-\lambda}"),
            (r"Bernoulli", r"\frac{S(n - S)}{n(n - 1)}", r"p(1 - p)"),
            (r"tanks", r"m(1 + \tfrac1k) - 1", r"N"),
        ]
        rows = VGroup()
        for nm, est, tgt in items:
            rows.add(VGroup(label(nm, font_size=24, color=GREY_A), MathTex(est, font_size=28, color=UMV),
                            MathTex(r"\text{for } " + tgt, font_size=28)))
        for r in rows:
            r[0].move_to([-4.0, 0, 0])
            r[1].move_to([1.0, 0, 0])
            r[2].move_to([4.6, 0, 0])
        rows.arrange(DOWN, buff=0.28).move_to([0, -1.3, 0])
        for r in rows:
            r[0].set_x(-4.0)
            r[1].set_x(1.0)
            r[2].set_x(4.6)
        intro = label('Completeness in full exponential families', font_size=36)
        with self.voiceover(
            "Where do complete statistics come from? <bookmark mark='a'/> Mostly from exponential families. If the "
            "density has the exponential-family form, and the natural parameters range over an open set, the "
            "sufficient statistic is complete. Part 45 proves it, using the uniqueness of Laplace transforms. "
            "<bookmark mark='b'/> So the best unbiased estimators of the textbook can be found by finding any "
            "unbiased function of the sufficient statistic. The sample mean, for a normal mean. The sample variance "
            "with n minus one, for a normal variance: Part 8's divisor is optimal among unbiased estimators. The "
            "Rao–Blackwellized quiet-year estimator of the last chapter: it can't be beaten either. The binomial "
            "variance, with its own small correction. And the tanks, which aren't an exponential family, but whose "
            "maximum we proved complete by hand."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def absurd(self):
        rows = [
            cmath(r"X \sim \text{Poisson}(\lambda),\quad \tau", r"=", r"e^{-2\lambda}", r"\quad\text{one observation}", font_size=32),
            cmath(r"E\,g(X) = \sum_x g(x)\frac{\lambda^x e^{-\lambda}}{x!}", r"=", r"e^{-2\lambda}\ \iff\ \sum_x g(x)\frac{\lambda^x}{x!} = e^{-\lambda}",
                  font_size=30),
            cmath(r"g(x)", r"=", r"(-1)^x", r"\quad\text{match the series of } e^{-\lambda}", font_size=32),
        ]
        rows[2][2].set_color(S.RESID)
        whys = [why(r"the chance of two quiet years in a row"), why(r"unbiasedness, \ written out"),
                why(r"the UMVUE: \ $+1$ or $-1$, \ an estimate of a probability")]
        foot = fit_rows(VGroup(
            label(r"the best unbiased estimator can be absurd; \ $\max(0, \cdot)$ is biased and better", font_size=26, color=S.ACCENT),
            label(r"unbiasedness is a constraint, \ not a virtue: \ chapter 11 lets bias back in", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.5, 0])
        intro = label('A best unbiased probability estimate can be negative', font_size=36)
        with self.voiceover(
            "But best unbiased doesn't always mean good. Here's a classic warning. <bookmark mark='a'/> One Poisson "
            "observation, and we want e to the minus two lambda, the chance of two quiet years in a row. "
            "<bookmark mark='b'/> An unbiased estimator g must satisfy this equation for every lambda. Multiply through "
            "by e to the lambda, and the left side is a power series in lambda that must equal e to the minus lambda. "
            "<bookmark mark='c'/> Match coefficients: g of x is minus one to the power x. That's the only unbiased "
            "estimator, so it's the UMVUE, and it estimates a probability as plus one or minus one. "
            "<bookmark mark='d'/> Simply replacing the negative values with zero gives a biased estimator that's "
            "never further from the truth, and strictly closer whenever the estimate was negative. <bookmark mark='e'/> Unbiasedness is a constraint we chose, not a virtue in "
            "itself, and chapter eleven lets bias back in."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
