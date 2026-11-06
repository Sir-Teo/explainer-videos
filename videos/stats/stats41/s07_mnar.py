from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class MNAR(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.heckman()
        self.mills()
        self.mroz_story()
        self.mroz_table()
        self.exclusion()
        self.bounds()
        self.pattern()
        self.tipping()
        self.practice()

    def card(self):
        card = chapter_card(6, r"Missing not at random", r"Model the reason, \ or measure how much it matters", lit=(1979,), part=PART)
        with self.voiceover("Chapter six. Missing not at random."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"wages are seen only for those who work", font_size=26, color=MNC),
            label(r"women in 1975 worked if their offered wage beat their reservation wage", font_size=26),
            label(r"so the observed wages are selected on the wage itself", font_size=26, color=MNC),
            label(r"two ways forward: \ model the selection, \ or bound its effect", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic case comes from economics. A wage is seen only for someone who works. "
            "<bookmark mark='b'/> In the 1970s many married women did not work for pay, and economists reasoned that a "
            "woman took a job when the wage she was offered beat the value of her time at home. <bookmark mark='c'/> So "
            "observed wages are selected on the wage itself: missing not at random. <bookmark mark='d'/> There are two ways "
            "forward: model the selection explicitly, or measure how much it could matter."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def heckman(self):
        rows = [
            cmath(r"y_i^*", r"=", r"x_i^\top \beta + \varepsilon_i: \ \text{the offered wage}", font_size=30),
            cmath(r"s_i^*", r"=", r"z_i^\top \gamma + u_i, \ \ s_i = 1\{s_i^* > 0\}: \ \text{working}", font_size=30),
            cmath(r"(\varepsilon, u)", r"\sim", r"N\Big(0, \begin{pmatrix} \sigma^2 & \rho\sigma \\ \rho\sigma & 1 \end{pmatrix}\Big)", font_size=30),
            cmath(r"E[y \mid x, s = 1]", r"=", r"x^\top \beta + \rho\sigma\, \lambda(z^\top \gamma), \ \ \lambda = \phi/\Phi", font_size=30),
        ]
        rows[3][-1].set_color(MNC)
        whys = [why(r"the outcome equation"), why(r"the selection equation"), why(r"correlated errors"), why(r"Heckman (1979)")]
        with self.voiceover(
            "<bookmark mark='a'/> James Heckman's model of 1979, for which he shared the Nobel prize. An outcome equation "
            "for the wage everyone is offered, <bookmark mark='b'/> a selection equation for whether one works, a probit, "
            "<bookmark mark='c'/> and errors that are jointly normal and correlated: unobserved ambition might raise both "
            "the wage and the chance of working. <bookmark mark='d'/> Then the mean observed wage is the regression plus a "
            "term rho sigma times the inverse Mills ratio of the selection index. Ordinary least squares on workers omits "
            "that term."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mills(self):
        A = axes([-3, 3], [0, 3.5], x_length=7.4, y_length=4.2, xlabel=r"selection index $z^\top\gamma$", ylabel=r"$\lambda = \phi / \Phi$",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        from scipy import stats as st
        xs = np.linspace(-3, 3, 200)
        c = polyline(ax, xs, st.norm.pdf(xs) / st.norm.cdf(xs), MNC, 3)
        side = fit_rows(VGroup(
            label(r"the inverse Mills ratio", font_size=22, color=MNC),
            label(r"large when selection was unlikely", font_size=22),
            label(r"near 0 when working was near certain", font_size=22, color=GREY_A),
            label(r"two steps: \ probit, \ then OLS with $\hat\lambda$ as a regressor", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The inverse Mills ratio, phi over Phi of the selection index. <bookmark mark='b'/> It is "
            "large for people who were unlikely to be selected, whose presence in the sample says their error must be "
            "unusually favourable; <bookmark mark='c'/> near zero for those who would almost surely be selected. <bookmark "
            "mark='d'/> Heckman's two-step method fits the probit, computes each worker's ratio, and adds it as a regressor; "
            "maximum likelihood fits both equations at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), Create(c), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def mroz_story(self):
        d = load("heckman")
        rows = fit_rows(VGroup(
            label(rf"Thomas Mroz (1987): \ {d['n']} married women in the 1975 Panel Study of Income Dynamics", font_size=26),
            label(rf"{d['n_work']} worked for pay; \ mean wage \${d['mean_wage']:.2f} an hour", font_size=26, color=OBSV),
            label(rf"with no child under 6: \ {100 * d['kids5_rate'][0]:.0f}\% worked; \ with one: \ {100 * d['kids5_rate'][1]:.0f}\%; \ with two: \ {100 * d['kids5_rate'][2]:.0f}\%", font_size=26, color=MNC),
            label(r"young children move women out of work, \ but should not change their offered wage", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Thomas Mroz's data of 1987, " + str(d["n"]) + " married women from the 1975 wave of the "
            "Panel Study of Income Dynamics. <bookmark mark='b'/> " + str(d["n_work"]) + " worked for pay. <bookmark "
            "mark='c'/> Of women with no child under six, " + str(round(100 * d["kids5_rate"][0])) + " percent worked; with "
            "one, " + str(round(100 * d["kids5_rate"][1])) + "; with two, " + str(round(100 * d["kids5_rate"][2])) + ". "
            "<bookmark mark='d'/> Young children strongly affect whether a woman works but, plausibly, not the wage she "
            "would be offered: an exclusion restriction, like Part thirty-seven's instruments."
        ) as vo:
            self.add(mroz_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mroz_table(self):
        d = load("heckman")
        rows = [[r"log wage on:", r"OLS, \ workers", r"Heckman, \ two steps", r"Heckman, \ ML"],
                [r"education \ (per year)", f"{d['ols']['beta'][1]:.4f}", f"{d['two']['beta'][1]:.4f}", f"{d['mle']['beta'][1]:.4f}"],
                [r"experience", f"{d['ols']['beta'][2]:.4f}", f"{d['two']['beta'][2]:.4f}", f"{d['mle']['beta'][2]:.4f}"],
                [r"$\hat\rho$", r"---", f"{d['two']['rho']:.3f}", f"{d['mle']['rho']:.3f}"]]
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.36, colors=[GREY_A, OBSV, MNC, MNC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"selection barely matters here: \ $\hat\rho$ is near zero", font_size=24, color=TAUC),
            label(r"each year of schooling raises wages about 11\% \ either way", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The results. <bookmark mark='b'/> Ordinary least squares on the workers says a year of "
            "education raises the wage by about " + str(round(100 * d["ols"]["beta"][1])) + " percent. Heckman's two steps "
            "and maximum likelihood agree. <bookmark mark='c'/> The estimated correlation is close to zero: for these "
            "women, whatever made them work was nearly unrelated to their wage, once education and experience are known. "
            "A famous model, and here a famous non-result, which is the most common outcome in practice."
        ) as vo:
            self.add(mroz_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(foot))
        self.clear_scene()

    def exclusion(self):
        rows = fit_rows(VGroup(
            label(r"without a variable that affects selection but not the outcome, \ $\lambda$ is nearly linear in $x$", font_size=26, color=MNC),
            label(r"then the model is identified only by the normal distribution's shape", font_size=26),
            label(r"so the answer rests on an untestable assumption, \ and the estimates are fragile", font_size=26, color=MNC),
            label(r"Little (1985), \ Manski (1989): \ treat selection models as sensitivity analyses", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Heckman's model needs care. Without a variable that shifts selection but not the outcome, "
            "the Mills ratio is almost a linear function of the regressors, <bookmark mark='b'/> and the model is "
            "identified only by the exact shape of the normal distribution. <bookmark mark='c'/> The answer then rests on an "
            "assumption no data can check, and the estimates swing widely. <bookmark mark='d'/> Roderick Little and Charles "
            "Manski urged treating selection models as one sensitivity analysis among several, not as the answer."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def pattern(self):
        rows = [
            cmath(r"\text{selection model}", r":", r"f(y)\, P(R \mid y)", font_size=32),
            cmath(r"\text{pattern mixture}", r":", r"P(R)\, f(y \mid R)", font_size=32),
            cmath(r"f(y \mid R = 0)", r"=", r"f(y \mid R = 1, x) \text{ shifted by } \delta", font_size=30),
            cmath(r"\delta", r":", r"\text{not estimable: \ chosen, \ and varied}", font_size=32),
        ]
        rows[2][-1].set_color(MNC)
        whys = [why(r"Heckman's factorization"), why(r"Little (1993)"), why(r"delta adjustment"), why(r"a sensitivity parameter")]
        with self.voiceover(
            "<bookmark mark='a'/> A selection model factors the joint distribution as the outcome times the chance of "
            "responding given it. <bookmark mark='b'/> A pattern-mixture model, Little's alternative, factors it the other "
            "way: the chance of each pattern, times the outcome's distribution within each pattern. <bookmark mark='c'/> "
            "The simplest version says the non-respondents look like similar respondents, shifted by an amount delta. "
            "<bookmark mark='d'/> Delta cannot be estimated from the data. It is chosen, and varied, and the analysis "
            "reports how the conclusion moves with it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tipping(self):
        d = load("tipping")
        R = d["rows"]
        dl = np.array([r["delta"] for r in R])
        est, lo, hi = (np.array([r[k] for r in R]) for k in ("est", "lo", "hi"))
        A = axes([0, 1], [10.3, 10.7], x_length=7.4, y_length=4.2, xlabel=r"$\delta$: \ how much richer the refusers are \ (log scale)",
                 ylabel=r"mean log income", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[10.3, 10.4, 10.5, 10.6, 10.7],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}", center=[-2.5, 0.2, 0])
        ax = A.ax
        bd = band(ax, dl, lo, hi, MNC, 0.25)
        c = polyline(ax, dl, est, MNC, 3)
        truth = DashedLine(ax.c2p(0, d["truth"]), ax.c2p(1, d["truth"]), color=TRUEC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"the MNAR mask: \ impute under MAR, \ then add $\delta$", font_size=22),
            label(r"$\delta = 0$: \ the MAR answer, \ far too low", font_size=22, color=MNC),
            label(rf"gold: \ the truth, \ reached near $\delta \approx {d['true_delta']:.1f}$", font_size=22, color=TRUEC),
            label(r"tipping point: \ the $\delta$ that flips the answer", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A tipping-point analysis on the World's not-at-random mask. Impute under missing at "
            "random, then add delta to every imputed log income, for a range of deltas. <bookmark mark='b'/> At delta zero, "
            "the answer is the MAR one, far too low. <bookmark mark='c'/> As delta grows the estimate rises, and it reaches "
            "the truth, which only the World knows, near delta of " + say(d["true_delta"], 1) + ": refusers earning about "
            "twice what similar respondents do. <bookmark mark='d'/> In a real study one reports the delta at which the "
            "conclusion would change, and asks whether so large a difference is plausible."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bd), Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(truth), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def practice(self):
        rows = fit_rows(VGroup(
            label(r"regulators now ask for it: \ estimands and sensitivity analyses \ (ICH E9(R1), \ 2019)", font_size=26, color=TAUC),
            label(r"trials: \ jump to reference, \ copy reference, \ tipping points for dropouts", font_size=26),
            label(r"surveys: \ follow up a sample of non-respondents, \ and learn $\delta$", font_size=26, color=MIC),
            label(r"the best fix for missing data is not to have it: \ design for follow-up", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Regulators now expect this: the international guideline on estimands of 2019 asks trials "
            "to state what is being estimated when patients stop treatment, and to show sensitivity analyses. <bookmark "
            "mark='b'/> Trials assume, for example, that dropouts on the drug behave like the control arm afterwards. "
            "<bookmark mark='c'/> Surveys can do better still, by chasing a random subsample of non-respondents to learn "
            "delta directly. <bookmark mark='d'/> And the best fix for missing data is the oldest: design the study so "
            "that less of it goes missing."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def bounds(self):
        rows = [
            cmath(r"Y \in [0, 1]", r":", r"\text{the missing could be anything in its range}", font_size=30),
            cmath(r"E\,Y", r"\in", r"\big[\, p\,\bar y_{\text{obs}}, \ p\,\bar y_{\text{obs}} + (1 - p) \,\big]", font_size=30),
            cmath(r"\text{width}", r"=", r"1 - p: \ \text{the missing share}", font_size=32),
            cmath(r"\text{assumptions}", r":", r"\text{narrow the bounds, \ one at a time}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"no assumption at all"), why(r"Manski (1989)"), why(r"honest, \ and wide"), why(r"Part 37's partial identification")]
        with self.voiceover(
            "<bookmark mark='a'/> At the other extreme, assume nothing. For an outcome between zero and one, the missing "
            "values could be anything in that range. <bookmark mark='b'/> So the mean is bounded below by assuming every "
            "missing value is zero, and above by assuming every one is one, where p is the share observed: Charles Manski's "
            "worst-case bounds. <bookmark mark='c'/> Their width is exactly the missing share, honest but often too wide to "
            "be useful. <bookmark mark='d'/> Each defensible assumption, such as that refusers are no less likely to vote "
            "than responders, narrows them, the partial identification of Part thirty-seven."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

