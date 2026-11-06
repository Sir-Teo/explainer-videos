from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class MinimaxTesting(VoiceoverScene):
    def construct(self):
        self.card()
        self.separation()
        self.chi2()
        self.sparse()
        self.vsest()
        self.chart()
        self.hc()

    def card(self):
        card = chapter_card(8, r"Minimax testing", r"How faint a signal can anyone detect?", lit=(1997, 2004), part=PART)
        with self.voiceover("Chapter eight. Minimax testing: how faint a signal can anyone detect?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def separation(self):
        rows = [
            cmath(r"H_0: \theta = 0 \ \ \text{vs} \ \ H_1: \|\theta\| \ge \rho, \ \theta \in \Theta", r":", r"\text{the separation } \rho", font_size=32),
            cmath(r"\rho^*", r"=", r"\text{the smallest } \rho \text{ at which some test has both errors} \le 0.05", font_size=32),
            cmath(r"\text{Sobolev } \alpha, \ \text{the sequence model}", r":", r"\rho^* \asymp \varepsilon^{4\alpha/(4\alpha + 1)}: \ \text{faster than estimation's } \varepsilon^{2\alpha/(2\alpha+1)}", font_size=28),
            cmath(r"\text{why}", r":", r"\text{detecting that } \theta \ne 0 \text{ is easier than saying what } \theta \text{ is}", font_size=30),
        ]
        rows[1][-1].set_color(LOWC)
        rows[2][-1].set_color(HYPC)
        whys = [why(r"a composite alternative"), why(r"the minimax separation rate"), why(r"Ingster (1982, \ 1993)"), why(r"testing $\ne$ estimation")]
        with self.voiceover(
            "<bookmark mark='a'/> Testing has its own minimax theory. Test whether the parameter is zero against the "
            "alternative that it is at least rho away, within a smoothness class. <bookmark mark='b'/> The minimax "
            "separation is the smallest rho at which some test keeps both its error probabilities below five percent. "
            "<bookmark mark='c'/> Yuri Ingster found it for Sobolev classes: epsilon to the four alpha over four alpha plus "
            "one, which is smaller than the estimation rate. <bookmark mark='d'/> Detecting that something is there is "
            "easier than saying what it is: the test can pool evidence over many coefficients that it could not estimate "
            "one by one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chi2(self):
        rows = [
            cmath(r"T", r"=", r"\textstyle\sum_{k \le N} (y_k^2 - \varepsilon^2): \ \ E\,T = \sum_{k \le N} \theta_k^2, \ \ \mathrm{SD}_0(T) = \sqrt{2N}\,\varepsilon^2", font_size=30),
            cmath(r"\text{detect when}", r":", r"\|\theta\|^2 \gtrsim \sqrt N \varepsilon^2 + \text{tail}(N) = \sqrt N \varepsilon^2 + C^2 N^{-2\alpha}", font_size=32),
            cmath(r"N \asymp \varepsilon^{-4/(4\alpha+1)}", r"\Rightarrow", r"\rho^2 \asymp \varepsilon^{8\alpha/(4\alpha+1)}", font_size=34),
            cmath(r"\text{the gain}", r":", r"\sqrt N \text{ instead of } N: \ \text{noise averages out in a sum of squares}", font_size=32),
        ]
        rows[2][-1].set_color(HYPC)
        whys = [why(r"Ingster's chi-square statistic"), why(r"signal vs.\ fluctuation"), why(r"balance them"), why(r"why testing is easier")]
        with self.voiceover(
            "<bookmark mark='a'/> Here is why. Ingster's test sums the first N squared observations, each corrected for the "
            "noise. Its mean is the signal's energy in those coordinates, and under the null its standard deviation is only "
            "root two N times epsilon squared. <bookmark mark='b'/> So the test detects when the energy exceeds root N epsilon "
            "squared, plus whatever the signal hides beyond N. <bookmark mark='c'/> Balancing the two gives the separation "
            "rate. <bookmark mark='d'/> An estimator pays N epsilon squared for N coordinates; a test pays only root N, "
            "because the noise in a sum of squares averages out. That square root is the whole difference between testing "
            "and estimation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sparse(self):
        rows = [
            cmath(r"X_i \sim (1 - \epsilon_n) N(0, 1) + \epsilon_n N(\mu_n, 1)", r",", r"i = 1, \dots, n", font_size=32),
            cmath(r"\epsilon_n = n^{-\beta}, \ \mu_n = \sqrt{2 r \log n}", r":", r"\text{a few, \ faint signals}", font_size=32),
            cmath(r"\text{detectable iff}", r":", r"r > \rho^*(\beta) = \begin{cases} \beta - \tfrac12 & \tfrac12 < \beta \le \tfrac34 \\ (1 - \sqrt{1 - \beta})^2 & \tfrac34 < \beta < 1 \end{cases}", font_size=30),
            cmath(r"\text{the boundary}", r":", r"\text{below it, \ every test is asymptotically powerless}", font_size=32),
        ]
        rows[2][-1].set_color(LOWC)
        whys = [why(r"the sparse mixture"), why(r"$n^{1-\beta}$ signals"), why(r"Ingster (1997); \ Jin (2003)"), why(r"a lower bound for tests")]
        with self.voiceover(
            "<bookmark mark='a'/> A cleaner case, important in genomics: n test statistics, almost all pure noise, a small "
            "fraction carrying a shift. <bookmark mark='b'/> Let the fraction be n to the minus beta and the shift the root of "
            "two r log n, so the signals are both rare and faint. <bookmark mark='c'/> Ingster and Jiashun Jin found the exact "
            "detection boundary: the mixture can be told from pure noise exactly when r exceeds a function rho star of beta, "
            "beta minus a half for moderately sparse signals and one minus the root of one minus beta, squared, for very "
            "sparse ones. <bookmark mark='d'/> Below the boundary, every test, of any kind, is asymptotically powerless."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def vsest(self):
        rows = [
            cmath(r"\text{estimate the sparse } \theta", r":", r"\text{signals must exceed } \sqrt{2\log n} \text{ to be found}", font_size=32),
            cmath(r"\text{detect that any exist}", r":", r"\mu = \sqrt{2r\log n}, \ r < 1, \ \text{still detectable above } \rho^*(\beta)", font_size=30),
            cmath(r"\beta < \tfrac12", r":", r"\text{dense: \ the sum } \textstyle\sum X_i \text{ detects even tiny shifts}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{knowing that something is there, \ without knowing where}", font_size=32),
        ]
        rows[1][-1].set_color(HYPC)
        whys = [why(r"chapter 4: \ thresholds"), why(r"the detectable region"), why(r"Part 33's global null"), why(r"genomics' everyday situation")]
        with self.voiceover(
            "<bookmark mark='a'/> Compare with estimation. To locate individual signals among n coordinates, each must exceed "
            "the root of two log n, chapter four's threshold. <bookmark mark='b'/> But to detect that some signals exist, "
            "shifts with r below one, too small to locate any single one, are enough, as long as r is above the boundary. "
            "<bookmark mark='c'/> And when the signals are dense, beta below a half, a simple sum detects even tiny shifts. "
            "<bookmark mark='d'/> There is a wide region where we can know that something is there without being able to say "
            "where, which is the everyday situation of genome-wide studies, and of Part thirty-three's global null."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("detect")
        b = np.asarray(d["betas"])
        A = axes([0.5, 1.0], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"sparsity $\beta$ \ ($\epsilon = n^{-\beta}$)", ylabel=r"strength $r$ \ ($\mu = \sqrt{2r\log n}$)",
                 xticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        bd = polyline(ax, b, d["boundary"], TRUTHC, 4)
        ok = VGroup()
        for g in d["grid"]:
            c = interpolate_color(ManimColor(LOWC), ManimColor(ADAPTC), g["hc"])
            ok.add(Dot(ax.c2p(g["beta"], g["r"]), radius=0.12, color=c))
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']:,}$, \ 150 samples per dot", font_size=22),
            label(r"white: \ the detection boundary $\rho^*(\beta)$", font_size=22, color=TRUTHC),
            label(r"dots: \ higher criticism's power, \ red 0 to green 1", font_size=22, color=ADAPTC),
            label(r"above the line: \ power rises; \ below: \ near 5\%", font_size=22, color=HYPC),
            label(r"at finite $n$ the boundary is soft", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The phase diagram, with ten thousand statistics. <bookmark mark='b'/> The white curve is "
            f"the detection boundary. <bookmark mark='c'/> Each dot is the simulated power of one test, higher criticism, at a "
            f"combination of sparsity and strength: red for powerless, green for certain detection. <bookmark mark='d'/> Above "
            f"the boundary the power climbs towards one; well below it, it stays near the five percent of a test that knows "
            f"nothing. <bookmark mark='e'/> At finite n the transition is gradual, but its location follows the theory."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ boundary exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in ok], lag_ratio=0.03), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hc(self):
        d = load("detect")
        g = {(x["beta"], x["r"]): x for x in d["grid"]}
        rows = [
            cmath(r"HC^*", r"=", r"\max_{i \le n/2} \frac{\sqrt n\,(i/n - p_{(i)})}{\sqrt{p_{(i)}(1 - p_{(i)})}}", font_size=34),
            cmath(r"\text{Tukey's idea, \ Donoho \& Jin (2004)}", r":", r"\text{the most surprising standardized excess of small } p\text{-values}", font_size=30),
            cmath(r"\text{adaptive}", r":", r"\text{optimal along the whole boundary, \ without knowing } \beta \text{ or } r", font_size=32),
            cmath(r"\beta = 0.9, \ r = 0.8", r":", rf"\text{{HC power }} {g[(0.9, 0.8)]['hc']:.2f}; \ \text{{the max test }} {g[(0.9, 0.8)]['max']:.2f}", font_size=32),
        ]
        rows[2][-1].set_color(ADAPTC)
        whys = [why(r"sorted $p$-values"), why(r"Part 33's $p$-value plots"), why(r"like Lepski, \ for tests"), why(r"very sparse: \ the max wins")]
        with self.voiceover(
            f"<bookmark mark='a'/> Higher criticism is John Tukey's idea, made precise by David Donoho and Jiashun Jin in 2004. "
            f"Sort the p-values, and at each rank compare the fraction of p-values below a level with what pure noise would "
            f"give, standardized. <bookmark mark='b'/> Take the most surprising excess. <bookmark mark='c'/> It needs no "
            f"knowledge of the sparsity or the strength, yet it is optimal along the whole detection boundary: the testing "
            f"counterpart of Lepski's adaptation. <bookmark mark='d'/> No test wins everywhere at finite n: in the very sparse "
            f"corner, beta point nine and r point eight, the simple maximum statistic has power {say(g[(0.9, 0.8)]['max'], 2)} "
            f"against higher criticism's {say(g[(0.9, 0.8)]['hc'], 2)}, while in the moderately sparse region higher criticism "
            f"is far ahead."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
