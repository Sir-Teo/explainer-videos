from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Slutsky(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorems()
        self.tstat()
        self.seen()
        self.trap()

    def card(self):
        card = chapter_card(9, r"Slutsky and continuous mapping", r"Rules for combining limits", part=PART)
        with self.voiceover("Chapter nine. Slutsky's theorem and the continuous mapping theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorems(self):
        cmt = theorem_card(r"Continuous mapping", r"if $X_n \xrightarrow{d} X$ \ (or $\xrightarrow{P}$) \ and $g$ is continuous, \ then "
                           r"$g(X_n) \xrightarrow{d} g(X)$ \ (or $\xrightarrow{P}$)", who=r"Mann \& Wald, 1943", color=SIM, width=9.6,
                           font_size=24)
        sl = theorem_card(r"Slutsky's theorem", r"if $X_n \xrightarrow{d} X$ \ and \ $Y_n \xrightarrow{P} c$, \ a constant, \ then "
                          r"$X_n + Y_n \xrightarrow{d} X + c$, \ $Y_n X_n \xrightarrow{d} cX$, \ $X_n / Y_n \xrightarrow{d} X / c$ \ "
                          r"($c \ne 0$)", who=r"Evgeny Slutsky, 1925", color=S.ACCENT, width=9.6, font_size=24)
        cons = definition_card(r"Consistent", r"an estimator $\hat\theta_n$ with $\hat\theta_n \xrightarrow{P} \theta$: \ the weak law "
                               r"makes $\bar X_n$ consistent for $\mu$; \ Part 9 makes it a standard", color=S.LIK, width=9.6,
                               font_size=24)
        grp = VGroup(cmt, sl, cons).arrange(DOWN, buff=0.4).move_to([0, -0.1, 0])
        intro = label('Combining limits', font_size=36)
        with self.voiceover(
            "Limits would be useless if we couldn't combine them. Two theorems let us. <bookmark mark='a'/> The "
            "continuous mapping theorem: if X n converges, in distribution or in probability, so does any continuous "
            "function of it, to the same function of the limit. Henry Mann and Abraham Wald proved it in 1943. "
            "<bookmark mark='b'/> Slutsky's theorem: if X n converges in distribution and Y n converges in "
            "probability to a constant, then their sum, product and ratio converge to what you'd expect. Evgeny "
            "Slutsky, better known to economists, published it in 1925. <bookmark mark='c'/> One more word. An "
            "estimator that converges in probability to the quantity it estimates is called consistent. The weak "
            "law says the sample mean is consistent for the population mean."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(grp[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def tstat(self):
        rows = [
            cmath(r"T_n", r"=", r"\frac{\bar X_n - \mu}{S_n/\sqrt n}", r"=", r"\underbrace{\frac{\sqrt n(\bar X_n - \mu)}{\sigma}}_{\to_d\ N(0,1)}"
                  r"\cdot \underbrace{\frac{\sigma}{S_n}}_{\to_P\ 1}", font_size=32),
            cmath(r"S_n^2", r"=", r"\frac{n}{n-1}\Big(\overline{X^2}_n - \bar X_n^2\Big)", r"\xrightarrow{P}", r"E X^2 - \mu^2 = \sigma^2",
                  font_size=32),
            cmath(r"T_n", r"\xrightarrow{d}", r"N(0, 1)", r"\qquad \text{for i.i.d. } X_i,\ 0<\sigma^2<\infty", font_size=32),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"split it: \ the CLT part times a correction"), why(r"the weak law for $X^2$ and $X$, \ then continuous mapping"),
                why(r"Slutsky: \ no normality needed")]
        note_ = label(r"Part 8: \ for normal data, \ $T_n$ is \emph{exactly} Student's $t_{n-1}$ for every $n$", font_size=24,
                      color=GREY_A).to_edge(DOWN, buff=0.25)
        intro = label('Estimating the unknown standard deviation', font_size=36)
        with self.voiceover(
            "Here's the most important use. <bookmark mark='a'/> In practice we don't know sigma, so we divide by the "
            "sample standard deviation instead. That's the t statistic. Split it into two factors: the standardized "
            "mean, which tends to a standard normal by the central limit theorem, and sigma over S n. "
            "<bookmark mark='b'/> S n squared is built from the averages of X squared and of X; by the finite-first-moment weak law for i.i.d. variables, "
            "both converge to their expectations, and by continuous mapping S n converges to sigma. So the second "
            "factor tends to one. <bookmark mark='c'/> By Slutsky, the t statistic tends to a standard normal, for "
            "i.i.d. data with finite, positive variance. <bookmark mark='d'/> For normal data, Part 8 will show it "
            "has Student's t distribution exactly, at every sample size."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.2, buff=0.95, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()

    def seen(self):
        d = load("slutsky")
        ed = np.asarray(d["edges"])
        panels = VGroup()
        for k, (key, title, c) in enumerate((("height_10", r"heights, \ $n = 10$", S.EST), ("income_10", r"incomes, \ $n = 10$", WORLD),
                                             ("income_100", r"incomes, \ $n = 100$", WORLD))):
            A = axes([-5, 5], [0, 0.5], x_length=3.8, y_length=2.6, xticks=[-4, -2, 0, 2, 4], center=[-4.4 + 4.4 * k, -0.4, 0])
            h = hist_bars(A.ax, ed, np.asarray(d[key]["hist"]), color=c, opacity=0.75)
            xs = np.linspace(-5, 5, 200)
            cv = curve(A.ax, xs, normal_pdf(xs), EXACT, 2.5)
            t = label(title, font_size=24).next_to(A, UP, buff=0.15)
            s = label(rf"95\% interval covers: \ {100 * d[key]['cover']:.1f}\%", font_size=20, color=GREY_A).next_to(A, DOWN, buff=0.15)
            panels.add(VGroup(A, h, cv, t, s))
        head = label(r"$T_n$ for samples from the World, \ against $N(0, 1)$", font_size=28).to_edge(UP, buff=0.5)
        take = label(r"Slutsky gives the limit, \ not the speed: \ for skewed data $T_n$ leans left \ (a big mean comes with a "
                     r"big $S_n$)", font_size=22, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        if take.width > 12.8:
            take.width = 12.8
        tag = simulated_tag(r"simulated: 20,000 samples each").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Let's see it. <bookmark mark='a'/> For samples of ten heights, the t statistic is already very close to "
            "normal; at ten, the t with nine degrees of freedom reference is a little wider, so the histogram's tails sit just above "
            "the curve. <bookmark mark='b'/> For incomes it's a different story. The t statistic leans hard to the "
            "left, because a sample that happens to include a high earner has both a big mean and a big standard "
            "deviation, and the second shrinks the ratio. <bookmark mark='c'/> With a hundred people it's still "
            "visibly skewed, and the interval still falls short. <bookmark mark='d'/> Slutsky tells us where "
            "the statistic ends up, not how fast it gets there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k]))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def trap(self):
        rows = VGroup(
            MathTex(r"X_n = Z \xrightarrow{d} N(0, 1), \qquad Y_n = -Z \xrightarrow{d} N(0, 1)", font_size=30),
            MathTex(r"\text{but } X_n + Y_n = 0, \ \text{not } N(0, 2)", font_size=30, color=BOUND),
            label(r"marginal limits alone do not determine a sum: \ they forget how the variables are joined", font_size=24, color=S.ACCENT),
            label(r"Slutsky needs one of them to converge to a \emph{constant}, \ which has only one way to be joined", font_size=24,
                  color=GREY_A),
            label(r"in general you need the \emph{joint} limit of $(X_n, Y_n)$: \ Part 5's lesson, \ again", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        intro = label('Marginal limits do not specify a joint law', font_size=36)
        with self.voiceover(
            "Why does Slutsky insist on a constant? <bookmark mark='a'/> Let X n be a standard normal Z, and Y n be "
            "minus Z. Both converge in distribution to a standard normal. <bookmark mark='b'/> Adding the two marginal normal laws as if they were independent would give variance two, but the marginal limits do not justify that independence. But their sum is "
            "zero, always. <bookmark mark='c'/> Convergence in distribution describes each variable alone; it forgets "
            "how they're joined. <bookmark mark='d'/> A constant can only be joined one way, which is why Slutsky's "
            "theorem works. <bookmark mark='e'/> In general you need the joint limit, which is Part 5's lesson in a "
            "new setting."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
