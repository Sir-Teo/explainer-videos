from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, EST, GOOD, PART, load, real_data

C_ = {r"\beta": EST, r"\gamma": EST}


class GMM(VoiceoverScene):
    def construct(self):
        g = load("gmm")
        self.card()
        self.method()
        self.euler(g)

    def card(self):
        c = chapter_card(2, r"GMM and the consumption Euler equation", r"Can a model of investors explain returns?",
                         lit=(1982,), part=PART)
        with self.voiceover("Chapter two. The generalized method of moments, and the consumption Euler equation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"\mathbb{E}\big[g(x_t, \theta)\big]", r"=", r"0", font_size=40),
                cmath(r"\hat\theta", r"=", r"\arg\min_\theta\ \bar g(\theta)^\top W\,\bar g(\theta)", font_size=40,
                      colors={r"\hat\theta": EST}),
                cmath(r"J", r"=", r"T\,\bar g(\hat\theta)^\top \hat S^{-1} \bar g(\hat\theta)", r"\sim", r"\chi^2_{q - p}",
                      font_size=40, colors={r"J": ALT})]
        whys = [why(r"a theory says some functions of the data average to zero: moment conditions"),
                why(r"choose the parameters that bring the sample averages closest to zero; optimal $W$ is the inverse "
                    r"of their long-run covariance"),
                why(r"with more conditions than parameters, the leftover is a test of the theory itself (Hansen 1982)")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-1.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "Many theories in finance don't give you a likelihood. They give you averages that should be zero. Lars "
            "Peter Hansen built an estimator on exactly that in 1982: the generalized method of moments. "
            "<bookmark mark='a'/> Choose the parameters that bring the sample averages of the moment conditions as "
            "close to zero as possible, weighting them by how noisy each one is. <bookmark mark='b'/> If you have more "
            "conditions than parameters, you can't make them all zero at once, and how far they stay from zero is a "
            "test of the theory: Hansen's J statistic. The method won him a share of the 2013 Nobel prize."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def euler(self, g):
        eq = cmath(r"\mathbb{E}_t\Big[\beta \Big(\frac{C_{t+1}}{C_t}\Big)^{-\gamma} R_{t+1}\Big]", r"=", r"1", font_size=40,
                   colors=C_).to_edge(UP, buff=0.5)
        expl = wrapped_label(r"an investor who could save one more dollar would be indifferent: the marginal utility "
                             r"given up today equals the discounted marginal utility of what the dollar buys later",
                             11.0, 22, GREY_A).next_to(eq, DOWN, buff=0.3)
        res = VGroup(
            label(r"instruments: a constant, last quarter's consumption growth and market return", font_size=21,
                  color=GREY_B),
            label(r"assets: the stock market and the T-bill, quarterly 1947--2020, in real terms", font_size=21,
                  color=GREY_B),
            MathTex(rf"\hat\beta = {g['beta']:.3f} \ ({g['se'][0]:.3f}), \quad \hat\gamma = {g['gamma']:.1f} \ ({g['se'][1]:.1f})",
                    font_size=32, color=EST),
            MathTex(rf"J = {g['J']:.1f},\ {g['df']}\ \text{{df}},\ p = {g['p_J']:.4f}", font_size=32, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        puzzle = VGroup(
            label(r"why it fails:", font_size=23, color=GREY_A),
            MathTex(rf"\text{{equity premium: }} {100 * g['equity_premium_q']:.1f}\% \text{{ a quarter}}", font_size=28),
            MathTex(rf"\text{{consumption growth: sd }} {100 * g['sd_g']:.1f}\%,\ \text{{corr. with stocks }} "
                    rf"{g['corr_g_rm']:.2f}", font_size=28),
            MathTex(rf"\gamma \approx \frac{{\mathbb{{E}}[R^e]}}{{\mathrm{{cov}}(\Delta c, R^e)}} \approx {g['hj_gamma']:.0f}",
                    font_size=32, color=BAD),
            label(r"the equity premium puzzle (Mehra and Prescott 1985)", font_size=21, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        both = VGroup(res, puzzle).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if both.width > 13.0:
            both.scale_to_fit_width(13.0)
        both.next_to(expl, DOWN, buff=0.5)
        src = real_data(r"FRED: real PCE per capita (A794RX0Q048SBEA), CPI; Kenneth French: market and T-bill")
        with self.voiceover(
            "Here is the most famous moment condition in finance. An investor who can save one more dollar, in "
            "stocks or in bills, should be indifferent at the margin: the discounted value of marginal utility "
            "tomorrow, times the return, should average one. With power utility, gamma is risk aversion and beta "
            "is patience. Hansen and Kenneth Singleton estimated it by GMM in 1982. <bookmark mark='a'/> Do it again "
            "on seventy-three years of American data: real consumption per person from the national accounts, the "
            f"stock market and the Treasury bill. Patience comes out near one, and risk aversion near "
            f"{g['gamma']:.0f}, with a standard error larger than the estimate. <bookmark mark='b'/> And the J test "
            "rejects the model decisively. <bookmark mark='c'/> The reason is simple to see. Stocks have earned about "
            "two percent a quarter more than bills, but consumption is smooth, and barely moves with the stock market. "
            "To justify the premium, investors would need a risk aversion in the hundreds. Rajnish Mehra and Edward "
            "Prescott called it the equity premium puzzle in 1985. Part twenty-three returns to what replaced this "
            "model."
        ) as vo:
            self.play(Write(eq), FadeIn(expl))
            vo.wait_until("a")
            self.play(FadeIn(res[0]), FadeIn(res[1]), FadeIn(src))
            self.play(FadeIn(res[2]))
            vo.wait_until("b")
            self.play(FadeIn(res[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in puzzle], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
