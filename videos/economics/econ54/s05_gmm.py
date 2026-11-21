from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403
from videos.economics.econ54.s03_logit import heat


class GMM(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The generalized method of moments", r"Can a model be estimated without being solved?",
             "Chapter four. The generalized method of moments.", lit={1982: r"Hansen; \ Hansen and Singleton"},
             scale=("household", "market"), horizon=("a decade",))
        self.derive()
        self.euler()
        self.jtest()

    def derive(self):
        eqs = VGroup(
            MathTex(r"\mathbb{E}\big[g(x_t, \theta_0)\big] = 0", font_size=40, color=THEORY),
            MathTex(r"\hat\theta = \arg\min_\theta \; \bar g(\theta)'\, W\, \bar g(\theta), \qquad "
                    r"\bar g(\theta) = \frac{1}{n}\sum_t g(x_t, \theta)", font_size=38, color=EST),
            MathTex(r"W = S^{-1}: \quad \operatorname{Var}(\hat\theta) \approx \frac{1}{n}\big(G' S^{-1} G\big)^{-1}",
                    r"\qquad J = n\, \bar g(\hat\theta)'\, S^{-1}\, \bar g(\hat\theta) \;\sim\; \chi^2_{m-k}",
                    font_size=36, color=THEORY),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.6)
        notes = VGroup(
            label(r"$m$ conditions the model says should hold on average, \ $k$ parameters, \ $m \geq k$",
                  font_size=20, color=GREY_A),
            label(r"$S$: \ how noisy each condition is, \ and how they move together; \ "
                  r"$G$: \ how they respond to $\theta$", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Hansen, \ Econometrica 50(4) (1982)", corner=DR, font_size=12)
        hc = history_card(1982, r"Lars Peter Hansen", r"``Large sample properties of generalized method of moments "
                          r"estimators'': \ estimate from what the model says should be zero on average",
                          color=THEORY, width=10.0, font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Maximum likelihood needs the whole probability model. Often an economic model tells you less, but "
            "something sharp: some quantity should be zero on average. <bookmark mark='a'/> Write those as moment "
            "conditions: functions of the data and the parameters whose expectation is zero at the true "
            "parameters. <bookmark mark='b'/> Lars Peter Hansen's generalized method of moments, of 1982, takes the "
            "sample averages of the conditions and chooses the parameters that make them as close to zero as "
            "possible, measured with a weighting matrix W. <bookmark mark='c'/> With more conditions than "
            "parameters, they cannot all be zero exactly, and the weighting matters. The best weights are the "
            "inverse of the conditions' covariance: noisy conditions count less, and conditions that move together "
            "are not counted twice. The variance of the estimate follows from how fast the conditions respond to "
            "the parameters. <bookmark mark='d'/> And because the extra conditions are over-identifying, the "
            "minimized objective is itself a test, Hansen's J: if the model is right, it is roughly chi-squared, "
            "with as many degrees of freedom as extra conditions."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(Write(eqs[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2][0], shift=UP * 0.1), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[2][1], shift=UP * 0.1))
        self.clear_scene()

    def euler(self):
        Gm = load("gmm")
        eq = MathTex(r"\mathbb{E}_t\!\left[\beta \left(\frac{C_{t+1}}{C_t}\right)^{-\gamma} R_{t+1} - 1\right] = 0"
                     r"\;\Longrightarrow\; \mathbb{E}\!\left[\left(\beta e^{-\gamma g_{t+1}} R_{t+1} - 1\right) "
                     r"z_t\right] = 0", font_size=34, color=THEORY).to_edge(UP, buff=0.5)
        bs, gs = np.array(Gm["grid_b"]), np.array(Gm["grid_g"])
        ax = plane([bs[0], bs[-1]], [gs[0], gs[-1]], center=LEFT * 1.8 + DOWN * 0.7, x_length=6.4, y_length=4.4,
                   xticks=[0.90, 0.94, 0.98, 1.02], yticks=[0, 2, 4, 6], xlabel=r"patience, \ $\beta$",
                   ylabel=r"risk aversion, \ $\gamma$", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        hm = heat(ax, bs, gs, -np.array(Gm["obj"]), hi_color=EST, depth=2000.0)
        truth = Cross(stroke_color=TRUTHC, stroke_width=3).scale(0.11).move_to(ax.ax.c2p(*Gm["truth"]))
        est = dot(ax, Gm["theta"][0], Gm["theta"][1], EST, 0.09)
        side = VGroup(
            label(r"$z_t$: \ anything known at $t$: \\ a constant, \ last period's \\ growth and returns",
                  font_size=18, color=GREY_A),
            label(rf"{Gm['T']:,} periods, \ two assets, \\ eight conditions, \ two parameters", font_size=18,
                  color=DATA),
            label(rf"$\hat\beta = {Gm['theta'][0]:.3f}$ \ ({Gm['se'][0]:.3f}) \\ $\hat\gamma = "
                  rf"{Gm['theta'][1]:.2f}$ \ ({Gm['se'][1]:.2f})", font_size=20, color=EST),
            label(rf"truth: \ {Gm['truth'][0]:.2f} \ and \ {Gm['truth'][1]:.0f}", font_size=19, color=TRUTHC),
            label(rf"the two estimates' correlation: \ {Gm['corr']:.2f}", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.4)
        tag = island_tag(r"simulated: \ the Island's returns and consumption", corner=DR, font_size=13)
        hc = history_card(1982, r"Lars Peter Hansen and Kenneth Singleton", r"the consumer's Euler equation, \ "
                          r"estimated from consumption and returns without solving the model", color=EST, width=10.0,
                          font_size=24).move_to(DOWN * 0.3)
        with self.voiceover(
            "The most famous use is Hansen and Kenneth Singleton's, from the same year. <bookmark mark='a'/> A "
            "household that can save in an asset gives up a unit of consumption today only if it expects the "
            "return, valued in tomorrow's marginal utility and discounted, to repay exactly one unit. That is "
            "Part twenty-three's Euler equation. Multiply it by anything the household knew at the time, and the "
            "average must still be zero: each instrument gives a moment condition. <bookmark mark='b'/> On the "
            f"Island we have {Gm['T']:,} periods of consumption growth and returns on two assets, a bond-like one "
            "and a risky one; with a constant and last period's values as instruments, that is eight conditions for "
            "two parameters. <bookmark mark='c'/> Here is the GMM objective over patience and risk aversion, bright "
            "where it is small. The estimates: beta "
            f"{Gm['theta'][0]:.3f}, risk aversion {Gm['theta'][1]:.2f}, against {Gm['truth'][0]:.2f} and "
            f"{Gm['truth'][1]:.0f} planted. <bookmark mark='d'/> Notice what we did not do: we never solved for "
            "the household's consumption rule, or said what its income process was. The Euler equation alone was "
            "enough. <bookmark mark='e'/> Notice, too, the long bright ridge: more patience and more risk aversion "
            "can stand in for each other, and the two estimates are strongly correlated. We met that ridge in the "
            "Play it, and we will meet it again."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(Write(eq), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(ax), FadeIn(hm), run_time=1.5)
            self.play(FadeIn(truth), FadeIn(est, scale=1.4), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Indicate(eq, color=WHITE, scale_factor=1.02))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def jtest(self):
        Gm = load("gmm")
        xs = np.array(Gm["chi_x"])
        ax = plane([0, 75], [0, 0.14], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50, 60, 70], yticks=[0, 0.05, 0.1], xlabel=r"Hansen's $J$",
                   ylabel=r"its distribution if the model is right", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        c1 = path(ax, xs, Gm["chi_pdf"], GAIN, 2.6, xr=(0, 75))
        c2 = path(ax, xs, Gm["bad_chi_pdf"], ERR, 2.6, xr=(0, 75))
        k1 = vline(ax, Gm["crit"], 0, 0.13, GAIN, 1.4)
        k2 = vline(ax, Gm["bad_crit"], 0, 0.13, ERR, 1.4)
        j1 = Triangle(fill_color=GAIN, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to(
            ax.ax.c2p(Gm["J"], 0.0) + UP * 0.2)
        j2 = Triangle(fill_color=ERR, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to(
            ax.ax.c2p(min(Gm["bad_J"], 74), 0.0) + UP * 0.2)
        side = VGroup(
            label(rf"two assets: \ $J = {Gm['J']:.1f}$, \\ {Gm['df']} degrees of freedom: \\ below the 5\% line, "
                  rf"\\ not rejected (p = {Gm['p_J']:.2f})", font_size=18, color=GAIN),
            label(rf"add an asset that pays \\ {100 * Gm['premium']:.0f} point a period more \\ than the model can "
                  rf"price: \\ $J = {Gm['bad_J']:.0f}$, \ {Gm['bad_df']} degrees of freedom: \\ rejected", font_size=18,
                  color=ERR),
            label(r"a rejection says the conditions \\ cannot all hold, \ not which one fails", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ the Island's returns and consumption", corner=DR, font_size=13)
        with self.voiceover(
            "Now the test. <bookmark mark='a'/> With two assets there are six more conditions than parameters, so "
            "if the model is right, J should look like a draw from the green curve. It is "
            f"{Gm['J']:.1f}, below the five percent line: the model is not rejected. <bookmark mark='b'/> Now add a "
            f"third asset whose return is {100 * Gm['premium']:.0f} percentage point a period higher than the model "
            "can explain: a premium the household's Euler equation does not price. There are now thirteen extra "
            f"conditions, and J jumps to {Gm['bad_J']:.0f}, far beyond the red line. The model is rejected. "
            "<bookmark mark='c'/> Two cautions. A rejection says the conditions cannot all hold at once; it does "
            "not say which one fails. And when Hansen and Singleton took the model to American stock returns, "
            "several of their specifications were rejected, an early sign of the trouble Part twenty-three called "
            "the equity premium puzzle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c1), Create(k1), run_time=1.2)
            self.play(FadeIn(j1, shift=DOWN * 0.2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c2), Create(k2), run_time=1.2)
            self.play(FadeIn(j2, shift=DOWN * 0.2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
