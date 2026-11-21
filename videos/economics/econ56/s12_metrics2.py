from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"A household's Euler equation is $\mathbb{E}_t\big[\beta\,(C_{t+1}/C_t)^{-\gamma} R_{j,t+1}\big] = 1$ for two "
    r"assets, \ $j = 1, 2$. \ You have $T = 2{,}000$ periods of consumption growth and both returns.",
    r"(a) \ Write moment conditions with instruments known at $t$: \ a constant, \ consumption growth and both "
    r"returns, \ each lagged once. \quad (8 marks)",
    r"(b) \ How many over-identifying restrictions are there? \quad (5 marks)",
    r"(c) \ Describe two-step GMM and the $J$ test, \ and report them. \quad (12 marks)",
]


class Metrics2(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Econometrics: \ GMM for an Euler equation", r"How do you estimate a model you cannot "
             r"solve?", "Question ten. Econometrics: GMM for an Euler equation.",
             lit={1982: r"Hansen; \ Hansen and Singleton", 2000: r"Hayashi"}, scale=("household",),
             horizon=("a year",))
        self.statement()
        self.solve()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(10, "metrics", r"GMM", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question ten. A household's Euler equation says that the discounted, marginal-utility-weighted gross "
            "return on each of two assets has expectation one. We have two thousand periods of data. <bookmark "
            "mark='a'/> Part a: moment conditions, using a constant and last period's consumption growth and "
            "returns as instruments. <bookmark mark='b'/> Part b: count the over-identifying restrictions. "
            "<bookmark mark='c'/> Part c: two-step GMM and the J test. Pause, and count the moments."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def solve(self):
        M = load("metrics2")
        one, two = M["one"], M["two"]
        tag = part_tag(10, "a--c", "metrics")
        rows = steps([
            (r"\mathbb{E}\Big[\big(\beta\, e^{-\gamma\,\Delta c_{t+1}} R_{j,t+1} - 1\big)\, z_t\Big] = 0, \quad "
             r"z_t = (1,\ \Delta c_t,\ R_{1,t},\ R_{2,t})",
             r"the Euler error is unpredictable from anything known at $t$"),
            (rf"m = 2 \times 4 = {M['m']}, \quad k = 2, \quad m - k = {M['df']}",
             r"(b) \ over-identifying restrictions", GAIN),
            (r"\hat\theta_1 = \arg\min_\theta\ \bar g(\theta)'\,\bar g(\theta)", r"(c) \ first step: \ identity "
             r"weights; \ consistent, \ not efficient"),
            (r"\hat S = \tfrac{1}{T}\sum_t g_t(\hat\theta_1)\, g_t(\hat\theta_1)', \quad \hat\theta_2 = "
             r"\arg\min_\theta\ \bar g'\,\hat S^{-1}\,\bar g", r"second step: \ weight each moment by its precision"),
            (rf"\hat\beta = {two['theta'][0]:.3f}\ ({two['se'][0]:.3f}), \quad \hat\gamma = {two['theta'][1]:.2f}\ "
             rf"({two['se'][1]:.2f})", r"truth 0.97 and 3; \ the first step's $\gamma$ had s.e. "
             rf"{one['se'][1]:.2f}", GAIN),
            (rf"J = T\,\bar g'\hat S^{{-1}}\bar g = {two['J']:.2f} \sim \chi^2_{{{M['df']}}}, \quad p = "
             rf"{two['p_J']:.2f}", r"the over-identifying restrictions are not rejected"),
        ], math_size=28, buff=0.28)
        rows.move_to(DOWN * 0.1)
        boxes = [answer_box(rows[1][0]), answer_box(rows[4][0])]
        with self.voiceover(
            "Part a. <bookmark mark='a'/> The Euler equation says the pricing error, beta times the growth of "
            "marginal utility times the return, minus one, cannot be predicted by anything known today. So it is "
            "uncorrelated with a constant, with last period's consumption growth and with last period's returns. "
            f"<bookmark mark='b'/> Part b. Four instruments for each of two assets: {M['m']} moment conditions for "
            f"two parameters, so {M['df']} over-identifying restrictions. <bookmark mark='c'/> Part c. The first "
            "step minimizes the plain sum of squared average moments: consistent, but it weights a noisy moment as "
            "much as a precise one. <bookmark mark='d'/> The second step estimates the moments' covariance at the "
            "first-step estimate and weights by its inverse, which is efficient. <bookmark mark='e'/> The estimates: "
            f"beta {two['theta'][0]:.3f} and gamma {two['theta'][1]:.2f}, with standard errors "
            f"{two['se'][0]:.3f} and {two['se'][1]:.2f}; the first step's standard error for gamma was "
            f"{one['se'][1]:.2f}. <bookmark mark='f'/> Hansen's J statistic, the sample size times the minimized "
            f"objective, is {two['J']:.2f} against a chi-square with {M['df']} degrees of freedom: a p-value of "
            f"{two['p_J']:.2f}, so the data do not reject the extra restrictions."
        ) as vo:
            self.play(FadeIn(tag))
            for k, (mk, r_) in enumerate(zip("abcdef", rows)):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if k == 1:
                    self.play(Create(boxes[0]))
                if k == 4:
                    self.play(Create(boxes[1]))
        self.clear_scene()

    def picture(self):
        M = load("metrics2")
        bs, gs, J = np.array(M["grid_b"]), np.array(M["grid_g"]), np.array(M["Jgrid"])
        th = M["two"]["theta"]
        ax = plane([bs[0], bs[-1]], [gs[0], gs[-1]], center=LEFT * 1.8 + DOWN * 0.3, x_length=6.6, y_length=5.4,
                   xticks=[0.96, 0.97, 0.98], yticks=[2.6, 3.0, 3.4], xlabel=r"$\beta$", ylabel=r"$\gamma$",
                   xfmt=lambda x: f"{x:.2f}", yfmt=lambda y: f"{y:.1f}", font_size=15)
        jmin = float(J.min())
        lv = np.log1p(J - jmin)
        lv = lv / lv.max()
        cells = VGroup()
        step = 2
        db, dg = (bs[1] - bs[0]) * step, (gs[1] - gs[0]) * step
        for i in range(0, len(gs), step):
            for j in range(0, len(bs), step):
                p0, p1 = ax.ax.c2p(bs[j] - db / 2, gs[i] - dg / 2), ax.ax.c2p(bs[j] + db / 2, gs[i] + dg / 2)
                inside = J[i, j] - jmin <= 5.99
                col = interpolate_color(ManimColor(METRICS), ManimColor("#151A24"), float(lv[i, j]))
                cells.add(Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), stroke_width=0,
                                    fill_color=GAIN if inside else col, fill_opacity=0.75 if inside else 0.9)
                          .move_to((p0 + p1) / 2))
        est = dot(ax, th[0], th[1], WHITE, 0.08)
        truth = Cross(stroke_color=EST, stroke_width=3).scale(0.12).move_to(ax.ax.c2p(M["beta"], M["gamma"]))
        side = VGroup(
            label(r"the $J$ objective over $(\beta, \gamma)$: \\ brighter is lower", font_size=19, color=METRICS),
            label(r"green: \ $J - J_{\min} \le 5.99$, \\ a 95\% confidence region", font_size=19, color=GAIN),
            label(r"white: \ the estimate; \\ gold cross: \ the truth", font_size=19, color=WHITE),
            label(r"a ridge: \ a higher $\beta$ \\ trades against a higher $\gamma$", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: \ 2{,}000 periods with $\beta = 0.97$, \ $\gamma = 3$", corner=DR,
                         font_size=13)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> The objective over a grid of beta and gamma: brighter is lower. "
            "<bookmark mark='b'/> In green, the parameters the J statistic does not reject at five percent: a "
            "confidence region. <bookmark mark='c'/> The estimate in white, and the truth, since these data are "
            "simulated, as a gold cross. <bookmark mark='d'/> The region is a tilted ridge: patience and risk "
            "aversion pull the same way on the average return, and only the instruments separate them. That "
            "ridge is why Hansen and Singleton's estimates on real data were so imprecise."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(cells, color=GAIN, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(est), FadeIn(truth), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"instruments dated $t + 1$: \ they must be known when the expectation is taken",
            r"the $J$ test with $m$ degrees of freedom: \ it is $m - k$",
            r"reporting first-step standard errors as if they were efficient",
            r"forgetting that GMM's consistency needs the moments to identify $\theta$: \ a flat ridge is weak "
            r"identification",
        ]).move_to(UP * 0.2)
        take = label(r"an orthogonality condition, \ counted and weighted, \ and tested if there are spare ones",
                     font_size=23, color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Instruments dated tomorrow. <bookmark mark='b'/> The J "
            "test with the wrong degrees of freedom. <bookmark mark='c'/> First-step standard errors reported as "
            "efficient. <bookmark mark='d'/> And forgetting that the moments must actually pin the parameters "
            "down. <bookmark mark='e'/> The idea to keep, from Part fifty-four: an orthogonality condition, "
            "counted, weighted, and tested when there are spare ones."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
