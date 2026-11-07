from __future__ import annotations

from videos.stats.stats53.common import *  # noqa: F403


class Misspecification(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.example()
        self.generalized()
        self.mueller()
        self.gibbs()
        self.board()
        self.safebayes()

    def card(self):
        card = chapter_card(11, r"Misspecification and generalized posteriors", r"When the model is wrong", lit=(2017,), part=PART)
        with self.voiceover("Chapter eleven. Misspecification and generalized posteriors: when the model is wrong."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\text{the truth } p_0 \notin \{p_\theta\}", r":", r"\theta^* = \arg\min_\theta \mathrm{KL}(p_0, p_\theta)", font_size=32),
            cmath(r"\text{the posterior}", r"\Rightarrow", r"N\big(\hat\theta, (nV_{\theta^*})^{-1}\big), \ \ V = -E\nabla^2 \log p_\theta", font_size=32),
            cmath(r"\text{the MLE}", r"\sim", r"N\big(\theta^*, V^{-1}JV^{-1}/n\big), \ \ J = \mathrm{Var}\,\nabla\log p_\theta: \ \text{the sandwich}", font_size=30),
            cmath(r"V^{-1} \ne V^{-1}JV^{-1}", r"\Rightarrow", r"\text{credible sets have the wrong size}", font_size=32),
        ]
        rows[3][-1].set_color(BADC)
        whys = [why(r"the best wrong model"), why(r"Kleijn \& van der Vaart (2012)"), why(r"Huber (1967), \ Part 22"), why(r"overconfident or not")]
        heading = label('Posterior convergence requires both local and global model conditions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> When the model is wrong, the truth is outside the family, and the best a model can do is the parameter closest to the truth in Kullback–Leibler divergence, as chapter two's boundary showed. <bookmark mark='b'/> Bas Kleijn and Aad van der Vaart proved in 2012 that under regularity, a unique interior KL minimizer, local nonsingular curvature and posterior concentration, the posterior is asymptotically normal there, with variance the inverse of the model's curvature over n. <bookmark mark='c'/> But the maximum likelihood estimator's actual variance is Huber's sandwich from Part twenty-two, which involves the variance of the score as well. <bookmark mark='d'/> When the two differ, credible sets have the wrong size: the posterior's centre is right and its spread is wrong."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def example(self):
        d = load("misspec")
        rows = [
            cmath(r"\text{counts with mean } 8, \ \text{variance } 40", r":", rf"\text{{negative binomial truth, \ }} n = {d['n']}", font_size=32),
            cmath(r"\text{a Poisson model}", r":", r"\text{variance} = \text{mean}: \ \text{it thinks the data five times less noisy}", font_size=30),
            cmath(r"\text{Gamma--Poisson posterior}", r":", rf"\text{{the right centre; \ width }} {d['w_plain']:.2f}", font_size=32),
            cmath(r"\text{coverage of 95\%}", r":", rf"{100 * d['cov_plain']:.1f}\%", font_size=36),
        ]
        rows[3][-1].set_color(BADC)
        whys = [why(r"overdispersed"), why(r"misspecified"), why(r"$\theta^* = $ the mean"), why(r"4,000 data sets")]
        heading = label('A Poisson working model understates overdispersed count uncertainty', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> An everyday example. Counts with mean eight and variance forty, two hundred of them, like "
            f"the overdispersed counts of Part twenty-four. <bookmark mark='b'/> Fit a Poisson model, which assumes the "
            f"variance equals the mean, and so believes the data five times less noisy than they are. <bookmark mark='c'/> "
            f"The conjugate posterior for the mean is centred correctly, since the KL-closest Poisson has the true mean, with "
            f"an average width of {say(d['w_plain'], 2)}. <bookmark mark='d'/> Its ninety-five percent credible intervals cover "
            f"the true mean only {100 * d['cov_plain']:.1f} percent of the time."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def generalized(self):
        d = load("misspec")
        rows = [
            cmath(r"\pi_\eta(\theta \mid X)", r"\propto", r"\pi(\theta)\, p(X \mid \theta)^\eta: \ \text{a tempered, \ generalized posterior}", font_size=30),
            cmath(r"\eta < 1", r":", r"\text{the likelihood counts for less: \ wider}", font_size=34),
            cmath(r"\text{calibrate}", r":", r"\hat\eta=\min(1,\bar y/s_y^2)\text{ in this scalar example}: \ \text{the spread matches the sandwich}", font_size=32),
            cmath(r"\text{here}", r":", rf"\hat\eta \approx {d['eta_true']:.1f}: \ \text{{width}} \ {d['w_tempered']:.2f}, \ \text{{coverage}} \ {100 * d['cov_tempered']:.1f}\%", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Bissiri, \ Holmes \& Walker (2016)"), why(r"a learning rate"), why(r"Lyddon et al.; \ Syring \& Martin"), why(r"finite experiment, \ not a uniform guarantee")]
        heading = label('Scalar tempering matches the leading spread in this one-dimensional model', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> The repair is a generalized posterior, Pier Giovanni Bissiri, Chris Holmes and Stephen Walker's framework of 2016: raise the likelihood to a power eta. <bookmark mark='b'/> With eta below one, the data count for less and the posterior widens. <bookmark mark='c'/> For this one-dimensional overdispersed Poisson working model, the plug-in mean-to-variance ratio matches the leading sandwich spread. One scalar learning rate cannot generally match a multivariate sandwich matrix. <bookmark mark='d'/> Here the estimated eta is about {say(d['eta_true'], 1)}; the intervals more than double in width, to {say(d['w_tempered'], 2)}, and cover {100 * d['cov_tempered']:.1f} percent."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mueller(self):
        rows = [
            cmath(r"\text{decision theory}", r":", r"\text{under misspecification, \ which posterior should one use?}", font_size=32),
            cmath(r"\text{Müller (2013)}", r":", r"\text{use the sandwich variance: \ lower risk}", font_size=32),
            cmath(r"\text{the sandwich posterior}", r":", r"N\big(\hat\theta, V^{-1}JV^{-1}/n\big): \ \text{centred like Bayes, \ sized like Huber}", font_size=30),
            cmath(r"\text{or}", r":", r"\text{fix the model: \ a negative binomial}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"asymptotic risk"), why(r"\emph{Econometrica}"), why(r"an artificial posterior"), why(r"the honest answer")]
        heading = label('A sandwich covariance adjustment depends on the decision problem', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Is tempering the right fix? Ulrich Müller asked the decision-theoretic question in 2013: if the model is wrong, which posterior minimizes the asymptotic risk of the decisions made from it? <bookmark mark='b'/> His answer: the one with the posterior's variance replaced by the sandwich. <bookmark mark='c'/> A sandwich posterior, centred like the Bayesian one and sized like Huber's. <bookmark mark='d'/> Or, often better, fix the model: a suitable negative-binomial model would address overdispersion, though its own prior and asymptotic calibration still need checking, and would have been the Bayesian's first choice once the overdispersion was noticed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gibbs(self):
        rows = [
            cmath(r"\text{no likelihood at all}", r":", r"\text{a median, \ a quantile, \ a classifier}", font_size=30),
            cmath(r"\pi_\eta(\theta \mid X)", r"\propto", r"\pi(\theta)\exp\big(-\eta\textstyle\sum_i \ell(\theta, X_i)\big)", font_size=34),
            cmath(r"\ell = |x - \theta|", r":", r"\text{a posterior for the median, \ with no model for the data}", font_size=32),
            cmath(r"\eta", r":", r"\text{calibrated by the bootstrap \ (Syring \& Martin 2019)}", font_size=34),
        ]
        rows[1][-1].set_color(PRIORC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"loss-based inference"), why(r"a Gibbs posterior"), why(r"robust, \ Part 30"), why(r"general posterior calibration")]
        heading = label('A loss-defined posterior still needs assumptions for calibration', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Sometimes there is no likelihood worth writing down, because the quantity of interest is defined by a loss: a median, a quantile, a classifier's error. <bookmark mark='b'/> A Gibbs posterior replaces the log-likelihood by minus eta times the summed loss. <bookmark mark='c'/> With absolute-error loss it is a posterior for the median that uses a loss instead of a parametric likelihood. Calibration still needs assumptions such as independent observations, a unique regular median, moments and bootstrap validity, the Bayesian analogue of Part thirty's robust estimators. <bookmark mark='d'/> Its learning rate can be calibrated by the bootstrap, as Nicholas Syring and Ryan Martin proposed in 2019, to target frequentist coverage under the calibration procedure's assumptions. It is not an exact distribution-free guarantee."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("Poisson credible", "tempered")
        d = load("misspec")
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Board: the Poisson posterior's interval for overdispersed counts covers "
                   f"{100 * d['cov_plain']:.1f} percent, broken. <bookmark mark='b'/> The tempered posterior's covers "
                   f"{100 * d['cov_tempered']:.1f} percent, kept.",
                   [("a", [0]), ("b", [1])])

    def safebayes(self):
        rows = fit_rows(VGroup(
            label(r"Choosing a learning rate for generalized posteriors", font_size=36, color=GREY_A),
            label(r"for calibration: \ match the sandwich, \ as here", font_size=26, color=GOODC),
            label(r"for prediction: \ Grünwald's SafeBayes picks $\eta$ to avoid overfitting a wrong model", font_size=26, color=PRIORC),
            label(r"Grünwald \& van Ommen (2017): \ standard Bayes can be inconsistent under misspecification", font_size=26, color=BADC),
            label(r"Gibbs posteriors: \ replace the log-likelihood by any loss \ (Part 54's PAC-Bayes)", font_size=26, color=BALLC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How should eta be chosen? <bookmark mark='b'/> For calibrated uncertainty, match the "
            "sandwich, as here. <bookmark mark='c'/> For prediction, Peter Grünwald's SafeBayes chooses eta to stop a wrong "
            "model from overfitting. <bookmark mark='d'/> Grünwald and Thijs van Ommen showed in 2017 that without it, a "
            "standard Bayesian linear regression with misspecified noise can be inconsistent, adding ever more spurious "
            "complexity. <bookmark mark='e'/> And replacing the log-likelihood by any loss gives Gibbs posteriors, the "
            "objects of Part fifty-four's PAC-Bayes bounds."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
