from __future__ import annotations

from videos.stats.stats48.common import *  # noqa: F403


class ZEstimators(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.example()
        self.table()
        self.newcomb()
        self.lesson()

    def card(self):
        card = chapter_card(8, r"Z-estimators with nuisance parameters", r"When estimating something else first costs, \ and when it does not", part=PART)
        with self.voiceover("Chapter eight. Z-estimators with nuisance parameters: when estimating something else first costs, and when it does not."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\hat\theta \text{ solves}", r":", r"P_n \psi_{\theta, \hat\eta} = 0, \ \ \hat\eta \text{ an estimated nuisance}", font_size=34),
            cmath(r"\{\psi_{\theta, \eta}\} \text{ Donsker}, \ \hat\eta \to \eta", r"\Rightarrow", r"\mathbb G_n \psi_{\hat\theta, \hat\eta} - \mathbb G_n \psi_{\theta_0, \eta_0} \to_P 0", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"\sqrt n(\hat\theta - \theta_0) = -V^{-1}\big(\mathbb G_n \psi_{\theta_0, \eta_0} + \sqrt n\, P\psi_{\theta_0, \hat\eta}\big) + o_P(1)", font_size=30),
            cmath(r"\sqrt n\, P\psi_{\theta_0, \hat\eta}", r"\approx", r"\partial_\eta P\psi_{\theta_0, \eta}\big|_{\eta_0} \cdot \sqrt n(\hat\eta - \eta_0)", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"plug in, \ then solve"), why(r"asymptotic equicontinuity, \ chapter 5"), why(r"van der Vaart (1998), \ Thm 5.21 and 25.54"), why(r"the nuisance's footprint")]
        heading = label('An estimated nuisance changes the population drift', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Many estimators solve an estimating equation that contains something else estimated first: a nuisance parameter, plugged in. <bookmark mark='b'/> If the estimating functions form a Donsker class and the nuisance estimate is consistent in the relevant L-two metric, asymptotic equicontinuity lets us replace the empirical process at the estimated values by the empirical process at the true ones: the random fluctuation is as if the nuisance were known. <bookmark mark='c'/> What remains is a deterministic drift: the population estimating equation evaluated at the estimated nuisance. <bookmark mark='d'/> To first order it is the derivative of the estimating equation in the nuisance, times the nuisance's own error. If that derivative is zero, the first-order drift vanishes. The higher-order remainder must still be little-oh of one over root n; with quadratic drift this often needs a nuisance rate faster than n to the minus one quarter. If not, its error is passed on."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def example(self):
        d = load("zest")["exact"]
        rows = [
            cmath(r"\theta(c)", r"=", r"E|X - c|: \ \text{the mean absolute deviation about } c", font_size=34),
            cmath(r"\partial_c\, \theta(c)", r"=", r"2F(c) - 1\quad(P\{X=c\}=0)", font_size=36),
            cmath(r"c = \text{the median}", r":", r"2F(m) - 1 = 0: \ \text{no footprint}", font_size=34),
            cmath(r"c = \text{the mean}, \ \text{Exp(1)}", r":", rf"2F(1) - 1 = 1 - 2/e = {d['mean']['slope']:.3f}: \ \text{{a footprint}}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"a centre, \ then a spread"), why(r"differentiate under $E$"), why(r"the median minimizes $E|X - c|$"), why(r"skewed data: \ $F(\mu) \ne 1/2$")]
        heading = label('Mean absolute deviation has a centre-dependent footprint', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> A simple example shows both cases. The mean absolute deviation about a centre c, distinct from the robust median absolute deviation: the expected distance from c. In practice c is estimated first. <bookmark mark='b'/> When F has no atom at c, its derivative in c is twice F of c minus one. <bookmark mark='c'/> If c is the median, that derivative is zero, because the median minimizes the mean absolute deviation. Under a regular continuous density and adequate convergence rates, estimating the median adds no first-order variance. <bookmark mark='d'/> If c is the mean of skewed data, it is not zero. For exponential data F of one is one minus one over e, and the slope is {say(d['mean']['slope'], 3)}. The error in the sample mean leaks into the estimate."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        z = load("zest")
        d, s = z["exact"], z["sim"]
        rows = [[r"centre", r"$n \times$ variance", r"centre known", r"centre estimated"],
                [r"median, \ $\log 2$", r"theory", f"{d['median']['naive']:.3f}", f"{d['median']['correct']:.3f}"],
                [r"", r"simulated", f"{s['median_known']:.3f}", f"{s['median_est']:.3f}"],
                [r"mean, \ 1", r"theory", f"{d['mean']['naive']:.3f}", f"{d['mean']['correct']:.3f}"],
                [r"", r"simulated", f"{s['mean_known']:.3f}", f"{s['mean_est']:.3f}"]]
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.36, colors=[GREY_B, None, EMPC, None, EMPC])
        tab.move_to([0, 0.8, 0])
        foot = label(rf"Exp(1) data, \ $n = {z['n']}$, \ 20,000 samples; \ theory by quadrature", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        ratio = d["mean"]["correct"] / d["mean"]["naive"]
        foot2 = label(rf"about the mean, \ ignoring the estimated centre understates the variance by a factor {ratio:.2f}", font_size=24, color=BADC).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The numbers, for two hundred exponential observations. About the median, the variance "
            f"is the same whether the median is known or estimated: {say(d['median']['naive'], 3)} in theory, "
            f"{say(s['median_known'], 3)} and {say(s['median_est'], 3)} simulated. About the mean, knowing the centre gives "
            f"{say(d['mean']['naive'], 3)}, but estimating it gives {say(d['mean']['correct'], 3)} in theory and "
            f"{say(s['mean_est'], 3)} in simulation. <bookmark mark='b'/> A standard error computed as if the centre were "
            f"known would understate the variance by a factor of {say(ratio, 2)}."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated: \ 20,000 samples; \ theory exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def newcomb(self):
        z = load("zest")
        nw = z["newcomb"]
        m, md = nw["mean"], nw["median"]
        rows = [
            cmath(rf"\text{{Newcomb's {z['nc_n']} passage times}}", r":", rf"\text{{MAD about the mean}} = {m['theta']:.2f}", font_size=32),
            cmath(r"\text{SE, \ centre treated as known}", r":", rf"{m['se_naive']:.2f}", font_size=34),
            cmath(r"\text{SE, \ with the footprint}", r":", rf"{m['se']:.2f}, \ \ \text{{slope }} 2F_n(\bar x) - 1 = {m['slope']:.2f}", font_size=32),
            cmath(r"\text{bootstrap SE}", r":", rf"{m['se_boot']:.2f}; \ \ \text{{about the median: }} {md['theta']:.2f} \pm {md['se']:.2f}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"Part 30's data"), why(r"$\mathrm{sd}(|x_i - \bar x| - \hat\theta)/\sqrt n$"), why(r"the outliers make $F_n(\bar x) \ne 1/2$"), why(r"4,000 resamples")]
        with self.voiceover(
            f"<bookmark mark='a'/> Real data. Simon Newcomb's sixty-six passage times of light, with their two outliers. The mean absolute deviation about the mean is {say(m['theta'], 2)}. <bookmark mark='b'/> Treating the centre as known, its standard error would be {say(m['se_naive'], 2)}. <bookmark mark='c'/> But the outliers drag the mean below the bulk of the data, so that only about forty-two percent of the points lie below it, and the slope twice F n of the mean minus one is {say(m['slope'], 2)}. Including the footprint raises the standard error to {say(m['se'], 2)}. <bookmark mark='d'/> The bootstrap, which re-estimates the centre in every resample automatically, gives {say(m['se_boot'], 2)}, closer to the corrected value. The median-centred calculation uses a continuous-population reference; the rounded data do not by themselves verify that model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.add(museum_tag(r"Newcomb (1882), \ via Stigler (1977)"))
        self.wait(0.5)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the general lesson: \ a plug-in's cost is its footprint, \ $\partial_\eta P\psi_{\theta_0, \eta}$", font_size=26),
            label(r"footprint zero: \ zero first-order drift; \ remainder rates still required", font_size=26, color=GOODC),
            label(r"footprint not zero: \ add the nuisance's influence function, \ or bootstrap the whole thing", font_size=26, color=BADC),
            label(r"chapter 12: \ the KS test with estimated parameters is the same story", font_size=26, color=CLASSC),
            label(r"Part 49: \ design the estimating function so that the footprint vanishes", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The general lesson: the cost of plugging in an estimated nuisance is its footprint, the derivative of the population estimating equation in the nuisance. <bookmark mark='b'/> When the footprint is zero, the first-order drift is absent, provided the remainder and empirical-process conditions hold. This property is called Neyman orthogonality. <bookmark mark='c'/> When it is not zero, add the nuisance's influence function to the estimator's, or bootstrap the whole two-step procedure. <bookmark mark='d'/> Chapter twelve's Kolmogorov–Smirnov test with estimated parameters is the same story in a function space. <bookmark mark='e'/> And Part forty-nine turns the lesson into a design principle: choose the estimating function so that the footprint vanishes, even when the nuisance is infinite dimensional."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
