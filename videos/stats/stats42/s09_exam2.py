from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403

LTOP = 1.45


class ExamBayes(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p4()
        self.p5()
        self.p6()

    def card(self):
        card = chapter_card(8, r"Exam II: \ Bayes and model choice", r"Problems 4--6", part=PART)
        with self.voiceover("Chapter eight. Three problems on Bayesian models, their computation, and choosing between models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 4
    def p4(self):
        d = load("p_hier")
        ys = ", ".join(f"{v:.0f}" for v in d["y"])
        ss = ", ".join(f"{v:.0f}" for v in d["s"])
        card = ExamCard(4, r"a posterior for a hierarchical model", r"Parts 25, 26", [
            rf"Rubin's eight schools: \ coaching effects $y_j$ = {ys}, \ standard errors $\sigma_j$ = {ss}.",
            r"With $y_j \sim N(\theta_j, \sigma_j^2)$, \ $\theta_j \sim N(\mu, \tau^2)$ and flat priors on $\mu$ and $\tau$,",
            r"find $p(\tau \mid y)$ up to a constant, \ and the posterior mean of school A's effect."], marks=12, color=POST)
        self.pose_voiceover(
            "Problem four. Rubin's eight schools: the estimated effects of coaching on a test in eight schools, each with its "
            "standard error. Model each estimate as normal around the school's true effect theta j, the true effects as "
            "normal around mu with spread tau, and put flat priors on mu and tau. Find the marginal posterior of tau up to a "
            "constant, and the posterior mean of school A's effect, whose estimate was twenty-eight points. Pause and try it.", card)
        rows = [
            cmath(r"y_j \mid \mu, \tau", r"\sim", r"N(\mu, \ \sigma_j^2 + \tau^2) \ \ \text{(integrate out } \theta_j)", font_size=30),
            cmath(r"p(\tau \mid y)", r"\propto", r"V_\mu^{1/2} \textstyle\prod_j (\sigma_j^2 + \tau^2)^{-1/2} \exp\!\Big(\!-\frac{(y_j - \hat\mu_\tau)^2}{2(\sigma_j^2 + \tau^2)}\Big)", font_size=28),
            cmath(r"\hat\mu_\tau", r"=", r"\frac{\sum_j w_j y_j}{\sum_j w_j}, \ \ w_j = \frac{1}{\sigma_j^2 + \tau^2}, \ \ V_\mu = \frac{1}{\sum_j w_j}", font_size=30),
            cmath(r"E[\theta_j \mid \tau, y]", r"=", r"(1 - B_j)\, y_j + B_j\, \hat\mu_\tau, \ \ B_j = \frac{\sigma_j^2}{\sigma_j^2 + \tau^2}", font_size=30),
        ]
        rows[1][-1].set_color(POST)
        whys = [why(r"normal-normal"), why(r"integrate out $\mu$, \ flat prior"), why(r"precision weights"), why(r"shrinkage")]
        with self.voiceover(
            "<bookmark mark='a'/> Integrate out each school's true effect: given mu and tau, each estimate is normal around "
            "mu with variance sigma j squared plus tau squared. <bookmark mark='b'/> Integrate out mu under its flat prior, "
            "completing the square, and the marginal posterior of tau is the root of V mu, times the product of the normal "
            "densities evaluated at mu hat. <bookmark mark='c'/> Here mu hat of tau is the precision-weighted mean of the "
            "estimates and V mu its variance. <bookmark mark='d'/> Given tau, each school's effect is shrunk from its own "
            "estimate towards mu hat by the factor B j, its sampling variance over its total variance. Averaging that over "
            "the posterior of tau, on a grid, gives the answer."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        tau, dens = np.asarray(d["tau"]), np.asarray(d["dens"])
        A = axes([0, 30], [0, 0.12], x_length=5.0, y_length=3.0, xlabel=r"$\tau$", ylabel=r"$p(\tau \mid y)$",
                 xticks=[0, 10, 20, 30], yticks=[0, 0.05, 0.1], center=[-4.0, -1.1, 0])
        ax = A.ax
        dc = density(ax, tau, np.minimum(dens, 0.12), POST)
        B = axes([0, 1], [-5, 30], x_length=3.6, y_length=3.4, xticks=[], yticks=[0, 10, 20, 30], center=[1.0, -1.0, 0])
        bx = B.ax
        lines = VGroup()
        for j in range(len(d["y"])):
            lines.add(VGroup(Line(bx.c2p(0, d["y"][j]), bx.c2p(1, d["theta"][j]), color=SCHOOL[j], stroke_width=2.5),
                             Dot(bx.c2p(0, d["y"][j]), radius=0.06, color=SCHOOL[j]), Dot(bx.c2p(1, d["theta"][j]), radius=0.06, color=SCHOOL[j])))
        heads = VGroup(label(r"$y_j$", font_size=22, color=GREY_A).next_to(bx.c2p(0, -5), DOWN, buff=0.15),
                       label(r"$E[\theta_j \mid y]$", font_size=22, color=GREY_A).next_to(bx.c2p(1, -5), DOWN, buff=0.15))
        side = fit_rows(VGroup(
            label(rf"$\tau$: \ median {d['tau_median']:.1f}, \ 90\% below {d['tau_q90']:.1f}", font_size=22, color=POST),
            label(rf"school A: \ 28 $\to$ {d['theta'][0]:.1f}", font_size=22, color=SCHOOL[0]),
            label(rf"pooled: \ {d['pooled']:.1f} \ (SE {d['pooled_se']:.1f})", font_size=22, color=GREY_A),
            label(r"partial pooling: \ between \emph{no} pooling and \emph{complete}", font_size=20, color=GREY_A),
        ), 3.6, 0.38, [5.0, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> On a grid, the posterior of tau piles up near zero but has a long tail: its median is "
            f"{say(d['tau_median'], 1)}, and ninety percent of it lies below {say(d['tau_q90'], 1)}. The data cannot rule out "
            f"that coaching works equally everywhere. <bookmark mark='b'/> Averaging the shrinkage over that posterior, "
            f"school A's twenty-eight becomes {say(d['theta'][0], 1)}. <bookmark mark='c'/> Every school is pulled towards "
            f"the pooled mean of {say(d['pooled'], 1)}, the noisier ones further, and the order is almost unchanged. "
            f"<bookmark mark='d'/> It is the compromise of Parts twenty-five and twenty-six, between treating the schools as "
            f"unrelated and treating them as identical, with the data choosing where to stand."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(heads), FadeIn(museum_tag(r"Rubin (1981): \ the eight schools")))
            vo.wait_until("a")
            self.play(FadeIn(dc), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l) for l in lines[1:]], lag_ratio=0.2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------ Problem 5
    def p5(self):
        d = load("p_mcmc")
        bad, good = d["bad"], d["good"]
        card = ExamCard(5, r"MCMC diagnostics", r"Part 27", [
            r"Four random-walk Metropolis chains target $\tfrac12 N(-3, 1) + \tfrac12 N(3, 1)$, \ started at $-6, -2, 2, 6$,",
            rf"proposal SD 0.4. \ After 2,000 iterations \ (half discarded): \ $\hat R = {bad['rhat']:.2f}$, \ bulk ESS $= {bad['ess_bulk']:.0f}$, \ acceptance {100 * bad['accept']:.0f}\%.",
            r"What do these numbers say, \ what went wrong, \ and what would you change?"], marks=8, color=S.TREAT)
        self.pose_voiceover(
            f"Problem five. Four random-walk Metropolis chains target an equal mixture of two normals, centred at minus three "
            f"and plus three. They start at minus six, minus two, two and six, with proposals of standard deviation point "
            f"four. After two thousand iterations, discarding the first half, R hat is {say(bad['rhat'], 2)}, the bulk "
            f"effective sample size is {bad['ess_bulk']:.0f}, and {100 * bad['accept']:.0f} percent of proposals were "
            f"accepted. What do these numbers say, what went wrong, and what would you change? Pause and try it.", card)
        rows = [
            cmath(r"\hat R", r"=", r"\sqrt{\frac{\frac{n-1}{n} W + \frac1n B}{W}} \ \ \text{(split, rank-normalized)}", font_size=30),
            cmath(r"1.45", r"\gg", r"1.01: \ \text{the chains disagree about the distribution}", font_size=30),
            cmath(r"\text{ESS}", r"=", rf"{bad['ess_bulk']:.0f}: \ \text{{4,000 draws worth eight independent ones}}", font_size=30),
            cmath(rf"{100 * bad['accept']:.0f}\%", r":", r"\text{steps too small to cross between the modes}", font_size=30),
        ]
        rows[1][-1].set_color(S.TREAT)
        whys = [why(r"between vs within"), why(r"Vehtari et al. (2021)"), why(r"autocorrelation"), why(r"aim for 20--50\%")]
        with self.voiceover(
            "<bookmark mark='a'/> R hat compares the variance between chains with the variance within them; when the chains "
            "have all forgotten their starts and explore the same distribution, it is one. <bookmark mark='b'/> At one point "
            "four five, far above the modern threshold of one point oh one, the chains are describing different "
            "distributions. <bookmark mark='c'/> An effective sample size of eight says the four thousand retained draws "
            "carry the information of eight independent ones. <bookmark mark='d'/> And an acceptance rate near ninety "
            "percent is the clue: the steps are so small that almost every one is accepted, and no chain can cross the "
            "valley between the modes."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        cols = [S.CTRL, S.TREAT, S.ALT, S.ACCENT]
        panels = VGroup()
        for i, (r, ttl) in enumerate([(bad, r"proposal SD 0.4"), (good, r"proposal SD 4")]):
            A = axes([0, 500], [-8, 8], x_length=5.4, y_length=2.6, xlabel=r"iteration $/ 4$", xticks=[0, 250, 500], yticks=[-6, -3, 0, 3, 6],
                     center=[-3.3 + 6.4 * i, -1.2, 0])
            ax = A.ax
            tr = np.asarray(r["trace"])
            lines = VGroup(*[polyline(ax, np.arange(tr.shape[1]), tr[c], cols[c], 1.5, 0.85) for c in range(4)])
            cap = label(rf"{ttl}: \ $\hat R = {r['rhat']:.2f}$, \ ESS $= {r['ess_bulk']:.0f}$, \ accept {100 * r['accept']:.0f}\%",
                        font_size=20, color=S.TREAT if i == 0 else GOODC).next_to(A, UP, buff=0.12)
            panels.add(VGroup(A, lines, cap))
        with self.voiceover(
            f"<bookmark mark='a'/> The traces show it. On the left, two chains live near minus three and two near plus "
            f"three, and none ever crosses. <bookmark mark='b'/> On the right, the same chains with proposals ten times "
            f"wider: about {100 * good['accept']:.0f} percent are accepted, every chain visits both modes many times, R hat "
            f"is {say(good['rhat'], 2)} and the effective sample size {good['ess_bulk']:.0f}. <bookmark mark='c'/> One "
            f"caution belongs in every answer: R hat can only compare what the chains found. Had all four started near "
            f"plus three, the slow sampler would have reported a perfect R hat and half the distribution would be missing. "
            f"Overdispersed starts, as here, are what exposed it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][2]), Create(panels[0][1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]), Create(panels[1][1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(panels[0][2]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------ Problem 6
    def p6(self):
        d = load("p_ic")
        rows_ = d["rows"]
        tab = table_rows([[r"degree", r"$k$", r"$\hat\ell$"]] + [[f"{r['d']}", f"{r['k']}", f"{r['ll']:.2f}"] for r in rows_],
                         font_size=20, col_buff=0.4, row_buff=0.1)
        card = ExamCard(6, r"AIC against BIC", r"Part 28", [
            rf"Polynomials of degree 1 to 5 for New York's ozone on temperature \ ($n = {d['n']}$ days) \ have $k$ parameters",
            r"and the maximized log-likelihoods in the table. \ Which degree does AIC choose? \ BIC?",
            r"If the truth is quadratic, \ how often does each choose it as $n \to \infty$?"], marks=10, color=AICC)
        self.pose_voiceover(
            f"Problem six. Polynomials of degree one to five are fitted to New York's daily ozone against temperature, on "
            f"{d['n']} days. Each has k parameters, counting the variance, and a maximized log-likelihood, in the table. "
            f"Which degree does AIC choose, and which does BIC? And if the truth were a quadratic, how often would each "
            f"criterion choose it as the sample grows? Pause and try it.", card)
        tab.next_to(card, DOWN, buff=0.3)
        self.play(FadeIn(tab))
        self.wait(2.0)
        self.play(FadeOut(tab))
        tab2 = table_rows([[r"degree", r"$k$", r"$\hat\ell$", r"AIC", r"BIC"]] +
                          [[f"{r['d']}", f"{r['k']}", f"{r['ll']:.2f}", f"{r['aic']:.2f}", f"{r['bic']:.2f}"] for r in rows_],
                          font_size=24, col_buff=0.55, row_buff=0.14).move_to([-2.6, -0.9, 0])
        ia = int(np.argmin([r["aic"] for r in rows_]))
        ib = int(np.argmin([r["bic"] for r in rows_]))
        side = fit_rows(VGroup(
            label(r"AIC $= -2\hat\ell + 2k$", font_size=24, color=AICC),
            label(rf"BIC $= -2\hat\ell + k \log n$, \ $\log {d['n']} = {np.log(d['n']):.2f}$", font_size=24, color=BICC),
            label(rf"AIC: \ degree {rows_[ia]['d']}", font_size=26, color=AICC),
            label(rf"BIC: \ degree {rows_[ib]['d']}", font_size=26, color=BICC),
        ), 4.6, 0.42, [4.45, -0.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> AIC is minus twice the log-likelihood plus two per parameter; <bookmark mark='b'/> BIC "
            f"charges log n per parameter, here {say(np.log(d['n']), 2)}. <bookmark mark='c'/> AIC is smallest at degree "
            f"{rows_[ia]['d']}: the cubic and quartic terms together lower minus twice the log-likelihood by "
            f"{2 * (rows_[3]['ll'] - rows_[1]['ll']):.1f}, more than the four they cost. <bookmark mark='d'/> BIC "
            f"is smallest at degree {rows_[ib]['d']}: at nearly five per parameter, only the quadratic term pays its way. "
            f"The criteria disagree, and both are doing what they were built to do."
        ) as vo:
            self.play(FadeIn(tab2))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
                if k == 2:
                    self.play(Indicate(tab2[ia + 1] if hasattr(tab2, "__getitem__") else tab2))
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        ns = np.log10(np.asarray(d["ns"], float))
        A = axes([1.2, 3.5], [0, 1], x_length=6.6, y_length=3.4, xlabel=r"sample size $n$", ylabel=r"P(choose the true quadratic)",
                 xticks=[2, 3], yticks=[0, 0.5, 1], log_x=True, xfmt=lambda v: f"{10 ** v:g}", center=[-2.6, -1.0, 0])
        ax = A.ax
        ca = polyline(ax, ns, d["p_aic"], AICC, 4)
        cb = polyline(ax, ns, d["p_bic"], BICC, 4)
        side2 = fit_rows(VGroup(
            label(r"600 simulations at each $n$; \ degrees 1--6", font_size=22, color=GREY_A),
            label(rf"AIC: \ levels off near {d['p_aic'][-1]:.2f}", font_size=24, color=AICC),
            label(rf"one extra term passes when $\chi^2_1 > 2$: \ {d['chi2_tail']:.3f}", font_size=22, color=AICC),
            label(rf"BIC: \ $\to 1$ \ ({d['p_bic'][-1]:.2f} at $n = {d['ns'][-1]:,}$)", font_size=24, color=BICC),
            label(r"BIC is consistent; \ AIC predicts better", font_size=24, color=GREY_A),
        ), 4.6, 0.36, [4.45, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The second half is theory, checked by simulation: a true quadratic, candidates of degree "
            f"one to six, six hundred data sets at each sample size. <bookmark mark='b'/> AIC's chance of choosing the truth "
            f"rises and then levels off near {say(d['p_aic'][-1], 2)}, <bookmark mark='c'/> because a needless term is "
            f"added whenever its likelihood-ratio statistic, chi-squared on one degree of freedom, exceeds two, which happens "
            f"{100 * d['chi2_tail']:.0f} percent of the time at any sample size. <bookmark mark='d'/> BIC's penalty grows with "
            f"log n, so that chance goes to zero, and BIC finds the truth with probability tending to one. <bookmark "
            f"mark='e'/> BIC is consistent; AIC is efficient for prediction, as Part twenty-eight showed. Name the goal "
            f"before naming the criterion."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(side2[0]))
            vo.wait_until("b")
            self.play(Create(ca), FadeIn(side2[1]))
            vo.wait_until("c")
            self.play(FadeIn(side2[2]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side2[3]))
            vo.wait_until("e")
            self.play(FadeIn(side2[4]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
