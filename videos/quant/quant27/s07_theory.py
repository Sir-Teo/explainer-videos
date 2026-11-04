from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COMPLEX, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, ask, fit_right, load


class Theory(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_model()
        self.spectrum(t["mp"])
        self.derive()
        self.limits()
        self.risk(t["risk"])
        self.misspecified(t["mis"])
        self.kernels(t["rff"])
        self.open_problems()
        self.question()

    def card(self):
        c = chapter_card(6, r"The theory of overparameterised prediction", r"Why can a model with more parameters than "
                         r"observations forecast at all, and when does it help?", part=PART)
        with self.voiceover("Chapter six, for the researcher. Chapters four and five showed a curve and an argument. "
                            "Here is the theorem behind both, proved, and checked against simulation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_model(self):
        rows = [cmath(r"y", r"=", r"Xb + \varepsilon,\quad X \in \mathbb R^{N \times P},\ X_{ij} \sim N(0, 1),\ "
                      r"|b|^2 = r^2,\ \operatorname{Var}\varepsilon_i = \sigma^2", font_size=30, colors={r"y": LINEAR}),
                cmath(r"\hat b_\lambda", r"=", r"\big(\hat\Sigma + \lambda I\big)^{-1} X^{\top}y / N,\qquad "
                      r"\hat\Sigma = X^{\top}X / N", font_size=30, colors={r"\hat b_\lambda": NET}),
                cmath(r"\hat b_0", r"=", r"\lim_{\lambda \downarrow 0} \hat b_\lambda = X^{+}y = "
                      r"\arg\min\{|b|:\ Xb = y\}\ \ (P > N)", font_size=30, colors={r"\hat b_0": COMPLEX}),
                cmath(r"R(\lambda)", r"=", r"\mathbb E\big[(x^{\top}\hat b_\lambda - x^{\top}b)^2\big] = "
                      r"\mathbb E\,|\hat b_\lambda - b|^2,\qquad P/N \to \gamma", font_size=30,
                      colors={r"R(\lambda)": HURDLE})]
        whys = [why(r"the cleanest model with the phenomenon: isotropic features, a signal of size $r^2$, noise "
                    r"$\sigma^2$; $\gamma = P/N$ is the complexity of Chapter 4"),
                why(r"ridge regression with penalty $\lambda$, written with the sample covariance $\hat\Sigma$"),
                why(r"as $\lambda \to 0$ with more parameters than data, ridge tends to the pseudo-inverse: of all "
                    r"the coefficient vectors that fit the data exactly, the shortest. This is 'ridgeless' regression"),
                why(r"the out-of-sample excess risk; with isotropic $x$ it is the squared error in $b$. Proportional "
                    r"asymptotics: $N, P \to \infty$ together, which is what makes the answer exact")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The model is the simplest one that shows everything. <bookmark mark='a'/> N observations of P features, "
            "independent standard normals, a coefficient vector of length r, and noise of variance sigma squared. "
            "<bookmark mark='b'/> Ridge regression, written with the sample covariance. <bookmark mark='c'/> Let the "
            "penalty go to zero with more parameters than observations and ridge becomes the pseudo-inverse: of all "
            "the coefficient vectors that fit the data exactly, the shortest. That is ridgeless regression, the "
            "interpolator of Chapter 4. <bookmark mark='d'/> And measure it by its out-of-sample risk, as N and P grow "
            "together with their ratio gamma fixed. In that limit the risk is not bounded or estimated. It is known "
            "exactly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def spectrum(self, mp):
        panels = VGroup()
        for g, col in (("0.25", LINEAR), ("0.8", HURDLE), ("2.0", COMPLEX)):
            m = mp[g]
            ev = np.asarray(m["eig"])
            xs, dens = np.asarray(m["x"]), np.asarray(m["density"])
            hi = float(xs[-1])
            top = float(min(max(dens.max(), 0.4) * 1.25, 3.0))
            ax_g = axes([0, hi], [0, top], x_length=3.7, y_length=2.6, xlabel=r"eigenvalue of $\hat\Sigma$",
                        ylabel=r"", xticks=[0, round(hi / 2, 1)], yticks=[], font_size=12)
            ax = ax_g.ax
            nb = 30
            h, e = np.histogram(ev[ev > 1e-9], bins=nb, range=(0, hi))
            h = h / len(ev) / (e[1] - e[0])
            w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=max(ax.c2p(0, min(v, top))[1] - ax.c2p(0, 0)[1], 0.001),
                                      stroke_width=0, fill_color=col, fill_opacity=0.6).move_to(
                [ax.c2p((e[i] + e[i + 1]) / 2, 0)[0], (ax.c2p(0, min(v, top))[1] + ax.c2p(0, 0)[1]) / 2, 0])
                for i, v in enumerate(h) if v > 0])
            dl = curve(ax, xs[dens > 0], np.minimum(dens[dens > 0], top), WHITE, stroke_width=2.5)
            edge = DashedLine(ax.c2p(m["edge"], 0), ax.c2p(m["edge"], top), color=BAD, stroke_width=2)
            cap = VGroup(MathTex(rf"\gamma = {float(g):g}", font_size=26, color=col),
                         MathTex(rf"\lambda_{{\min}} = {m['min_eig']:.3f}" + (rf",\ \ \text{{atom}}\ {m['atom']:.0%}"
                                 .replace("%", r"\%") if m["atom"] > 0 else ""), font_size=20)).arrange(
                DOWN, buff=0.1)
            panels.add(VGroup(cap, VGroup(ax_g, bars, dl, edge)).arrange(DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.35).move_to(UP * 0.3)
        if panels.width > 13.2:
            panels.scale_to_fit_width(13.2)
        law = MathTex(r"dF_\gamma(s) = \frac{\sqrt{(b - s)(s - a)}}{2\pi\gamma s}\,ds,\quad a, b = (1 \mp \sqrt\gamma)^2",
                      font_size=30).to_edge(DOWN, buff=0.75)
        foot = note(r"bars: one draw, $N = 400$; white: Marchenko and Pastur (1967); red: the lower edge $a$. For "
                    r"$\gamma > 1$, $1 - 1/\gamma$ of the eigenvalues are exactly zero", font_size=16,
                    color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Everything runs through one object: the eigenvalues of the sample covariance. The true covariance is the "
            "identity, every eigenvalue one. <bookmark mark='a'/> The sample's are not. With a quarter as many "
            "features as observations they spread from a quarter to more than two. <bookmark mark='b'/> As gamma "
            "approaches one, the spread widens and the smallest eigenvalue slides towards zero: the lower edge of the "
            "Marchenko-Pastur law is one minus root gamma, squared. <bookmark mark='c'/> Past one, a share of the "
            "eigenvalues is exactly zero: directions the data say nothing about. Inverting a matrix with eigenvalues "
            "near zero multiplies the noise by their inverse. That, in one picture, is the spike of Chapter 4."
        ) as vo:
            self.play(FadeIn(law))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\hat b_\lambda - b", r"=", r"-\lambda(\hat\Sigma + \lambda I)^{-1} b + (\hat\Sigma + \lambda I)^{-1}"
                      r"X^{\top}\varepsilon / N", font_size=30, colors={r"\hat b_\lambda - b": NET}),
                cmath(r"R(\lambda)", r"=", r"\lambda^2\, b^{\top}(\hat\Sigma + \lambda I)^{-2} b + \tfrac{\sigma^2}{N}"
                      r"\operatorname{tr}\big[\hat\Sigma(\hat\Sigma + \lambda I)^{-2}\big]", font_size=30,
                      colors={r"R(\lambda)": HURDLE}),
                cmath(r"b^{\top} A\, b", r"\approx", r"\tfrac{r^2}{P}\operatorname{tr} A", font_size=30,
                      colors={r"b^{\top} A\, b": LINEAR}),
                cmath(r"\tfrac1P \operatorname{tr} f(\hat\Sigma)", r"\to", r"\textstyle\int f(s)\, dF_\gamma(s)",
                      font_size=30, colors={r"\tfrac1P \operatorname{tr} f(\hat\Sigma)": COMPLEX}),
                cmath(r"R(\lambda)", r"\to", r"r^2\lambda^2\!\textstyle\int\!\frac{dF_\gamma(s)}{(s + \lambda)^2} + "
                      r"\sigma^2\gamma\!\int\!\frac{s\, dF_\gamma(s)}{(s + \lambda)^2}", font_size=30,
                      colors={r"R(\lambda)": HURDLE})]
        whys = [why(r"substitute $X^{\top}y/N = \hat\Sigma b + X^{\top}\varepsilon/N$ and use "
                    r"$(\hat\Sigma + \lambda)^{-1}\hat\Sigma = I - \lambda(\hat\Sigma + \lambda)^{-1}$"),
                why(r"square and take expectations over $\varepsilon$: the cross term vanishes; the first is the "
                    r"squared bias, the second the variance"),
                why(r"rotation invariance: the law of $X$ does not change under $X \mapsto XO$, so only $b$'s length "
                    r"matters, and a quadratic form in a direction uniform on the sphere concentrates at the trace"),
                why(r"Marchenko--Pastur: the eigenvalue distribution of $\hat\Sigma$ converges to $F_\gamma$, so "
                    r"normalised traces become integrals (and $\tfrac{\sigma^2}{N}\operatorname{tr} = "
                    r"\sigma^2\gamma\cdot\tfrac1P\operatorname{tr}$)"),
                why(r"Hastie, Montanari, Rosset and Tibshirani (2022), Thm.\ 5 (and Dobriban and Wager 2018): the risk of "
                    r"ridge is a deterministic function of $(\gamma, \lambda, r^2, \sigma^2)$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Now the proof, in five lines. <bookmark mark='a'/> Substitute the model into the estimator. The error "
            "splits into a part that shrinks the true coefficients towards zero, which the penalty causes, and a "
            "part that is filtered noise. <bookmark mark='b'/> Square it and average over the noise: the cross term "
            "vanishes, leaving a squared bias and a variance. <bookmark mark='c'/> The bias is a quadratic form in "
            "the unknown b. Because the law of standard normal data is unchanged by any rotation, only b's length "
            "can matter, and the quadratic form concentrates at its trace. <bookmark mark='d'/> Both terms are now "
            "normalised traces of functions of the sample covariance, and by Marchenko and Pastur those converge to "
            "integrals against the law we just saw. <bookmark mark='e'/> So the risk of ridge, in the limit, is a "
            "deterministic function of four numbers: the complexity, the penalty, the signal and the noise."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def limits(self):
        body = VGroup(
            MathTex(r"\gamma < 1:\quad R(0^+) = \sigma^2\,\frac{\gamma}{1 - \gamma}", font_size=32),
            MathTex(r"\gamma > 1:\quad R(0^+) = \underbrace{r^2\big(1 - \tfrac1\gamma\big)}_{\text{bias}} + "
                    r"\underbrace{\sigma^2\,\frac{1}{\gamma - 1}}_{\text{variance}}", font_size=32),
            MathTex(r"\lambda^* = \sigma^2\gamma / r^2:\quad R(\lambda^*)\ \text{increases in}\ \gamma,\ \text{no spike}",
                    font_size=28, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        thm = theorem_card(r"The ridgeless risk", body,
            who=r"Hastie, Montanari, Rosset and Tibshirani (2022); Belkin, Hsu, Ma and Mandal (2019); Bartlett, Long, "
                r"Lugosi and Tsigler (2020)", width=10.4, font_size=24).move_to(UP * 0.3)
        whys = VGroup(
            why(r"below one: $\int s^{-1} dF_\gamma = 1/(1 - \gamma)$, so the variance explodes as the smallest "
                r"eigenvalue reaches zero; there is no bias, since the fit is unpenalised"),
            why(r"above one: the zero eigenvalues are the directions the interpolator cannot see, so $1 - 1/\gamma$ "
                r"of the signal is lost to bias, while the variance falls like $1/(\gamma - 1)$: the second descent"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        for w in whys:
            if w.width > 12.6:
                w.scale_to_fit_width(12.6)
        with self.voiceover(
            "Let the penalty go to zero. <bookmark mark='a'/> Below the interpolation threshold, the bias vanishes and "
            "the variance is sigma squared times gamma over one minus gamma, which explodes as the smallest eigenvalue "
            "reaches zero. Above it, the zero eigenvalues are directions the interpolator cannot see, so a share one "
            "minus one over gamma of the signal is lost to bias, while the variance falls like one over gamma minus "
            "one. That falling variance is the second descent. <bookmark mark='b'/> And with the best penalty, sigma "
            "squared gamma over r squared, there is no spike at all: optimally tuned ridge is never hurt by the "
            "threshold. The spike is a property of not regularising, not of complexity."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(whys))
            vo.wait_until("b")
            self.play(Indicate(body[2], color=GOOD, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def risk(self, r):
        gs = np.asarray(r["gamma"])
        top = 4.0
        g = axes([0, 10], [0, top], x_length=9.4, y_length=4.6, xlabel=r"$\gamma = P/N$",
                 ylabel=r"out-of-sample excess risk, $r^2 = \sigma^2 = 1$", xticks=[0, 1, 2, 5, 10],
                 yticks=[0, 1, 2, 3, 4], font_size=14).move_to(LEFT * 1.4 + DOWN * 0.25)
        ax = g.ax
        lo, hi = gs < 1, gs > 1

        def seg(y, col, sw=3, dash=False):
            y = np.minimum(np.asarray(y, float), top)
            parts = VGroup(curve(ax, gs[lo], y[lo], col, stroke_width=sw), curve(ax, gs[hi], y[hi], col, stroke_width=sw))
            return parts
        rl = seg(r["ridgeless"], COMPLEX)
        bias = curve(ax, gs[hi], np.minimum(np.asarray(r["bias"])[hi], top), LINEAR, stroke_width=2)
        var = seg(r["var"], BAD, sw=2)
        opt = curve(ax, gs, np.minimum(np.asarray(r["optimal"]), top), GOOD, stroke_width=3)
        null = DashedLine(ax.c2p(0, r["null"]), ax.c2p(10, r["null"]), color=GREY_B, stroke_width=1.5)
        thr = DashedLine(ax.c2p(1, 0), ax.c2p(1, top), color=HURDLE, stroke_width=1.5)
        dots = VGroup()
        for k, col in (("ridgeless", COMPLEX), ("optimal", GOOD)):
            for gm, s in zip(r["sim_gamma"], r["sim"][k]):
                if s["median"] > top:
                    continue
                dots.add(VGroup(Line(ax.c2p(gm, min(s["lo"], top)), ax.c2p(gm, min(s["hi"], top)), color=col,
                                     stroke_width=2), Dot(ax.c2p(gm, s["median"]), radius=0.06, color=col)))
        leg = legend([(COMPLEX, r"ridgeless, theory"), (LINEAR, r"its bias"), (BAD, r"its variance"),
                      (GOOD, r"optimal ridge, theory"), (GREY_B, r"predicting zero")], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.2)
        fit_right(leg)
        side = wrapped_label(rf"dots and bars: simulation, $N = {r['N']}$, median and 10--90\% of 30 draws. The "
                             r"formula is exact in the limit and already right at $N = 200$", 3.3, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Here is the theorem against the experiment. <bookmark mark='a'/> The ridgeless risk: rising to infinity "
            "at gamma equals one, then falling. Split above the threshold into its two parts, the bias rising towards "
            "the full signal and the variance falling away. <bookmark mark='b'/> The dots are simulations with two "
            "hundred observations, thirty draws each, and they sit on the formula. <bookmark mark='c'/> The optimal "
            "ridge, in green, never spikes, and always beats the grey line, the risk of simply predicting zero. But "
            "the interpolator never does, at any gamma above one: it approaches the grey line from above. In this "
            "model, where a fixed signal is spread over ever more features, more parameters only make the problem "
            "harder, and even the best ridge gets worse as gamma grows. The second descent recovers from the spike; "
            "it does not, here, create value. For that we need one more ingredient."
        ) as vo:
            self.play(FadeIn(g), Create(null), Create(thr), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(rl), run_time=2)
            self.play(Create(bias), Create(var))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05), FadeIn(side))
            vo.wait_until("c")
            self.play(Create(opt), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def misspecified(self, m):
        gs = np.asarray(m["gamma"])
        lo_, hi_ = gs < 1, gs > 1
        top = m["null"] + 1.5
        bot = m["null"] - 0.4
        g = axes([0, 10], [bot, top], x_length=9.0, y_length=4.2, xlabel=r"$\gamma = P/N$, of $P_{\text{total}} = 10N$ "
                 r"features", ylabel=r"total out-of-sample MSE", xticks=[0, 1, 2, 5, 10],
                 yticks=[round(m["null"] - 0.25, 2), m["null"], m["null"] + 1], font_size=14).move_to(
            LEFT * 1.4 + DOWN * 0.5)
        ax = g.ax
        y = np.clip(np.asarray(m["ridgeless"]), bot, top)
        rl = VGroup(curve(ax, gs[lo_], y[lo_], COMPLEX, stroke_width=3), curve(ax, gs[hi_], y[hi_], COMPLEX,
                                                                                stroke_width=3))
        opt = curve(ax, gs, np.clip(np.asarray(m["optimal"]), bot, top), GOOD, stroke_width=3)
        null = DashedLine(ax.c2p(0, m["null"]), ax.c2p(10, m["null"]), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(gm, s["median"]), radius=0.06, color=COMPLEX) for gm, s in
                        zip(m["sim_gamma"], m["sim"]) if bot < s["median"] < top])
        end = float(m["ridgeless"][-1])
        r2_end = 1 - end / m["null"]
        r2_opt = 1 - float(m["optimal"][-1]) / m["null"]
        und = float(np.min(np.asarray(m["ridgeless"])[lo_]))
        rows = [cmath(r"y", r"=", r"x_{1:P}^{\top} b_{1:P} + \underbrace{x_{P+1:}^{\top}b_{P+1:} + \varepsilon}_{"
                      r"\text{noise to a learner that sees } P}", font_size=28, colors={r"y": LINEAR})]
        rows[0].to_edge(UP, buff=0.35)
        side = VGroup(
            MathTex(rf"\text{{best}}\ \gamma < 1:\ {und:.2f}", font_size=24, color=COMPLEX),
            MathTex(rf"\text{{ridgeless}},\ \gamma = 10:\ {end:.2f}\ \ (R^2\ {100 * r2_end:.1f}\%)", font_size=24,
                    color=COMPLEX),
            MathTex(rf"\text{{optimal ridge}}:\ R^2\ {100 * r2_opt:.1f}\%", font_size=24, color=GOOD),
            MathTex(rf"\text{{predicting zero}}:\ {m['null']:.2f}", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        fit_right(side)
        foot = note(rf"$r^2 = {m['r2']:g}$, $\sigma^2 = 1$; dots: simulation, $N = 200$, 20 draws. Hastie et al.\ (2022), "
                    r"Sec.\ 5; Kelly, Malamud and Zhou (2024) prove the timing version", font_size=15,
                    color=GREY_B).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The ingredient is misspecification. <bookmark mark='a'/> Suppose the truth uses many more features than "
            "any model can afford, ten times the number of observations, and a model with P of them sees only that "
            "share of the signal. To it, the rest is noise. <bookmark mark='b'/> Now every model below the threshold "
            "is worse than predicting zero: it sees too little of the signal to pay for its variance. Past the "
            "spike, the ridgeless interpolator keeps adding signal faster than variance, and with all the features it "
            "beats predicting zero, with an out-of-sample R squared of about three percent. Optimal ridge does a "
            "little better. <bookmark mark='c'/> This is the virtue of complexity, exactly: not that interpolation is "
            "magic, but that when the truth is complex, a model must be large to see it, and a large model, "
            "sensibly shrunk, pays its way. Kelly, Malamud and Zhou prove the timing version; whether returns are "
            "like this is the empirical question Nagel raised."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(null))
            vo.wait_until("b")
            self.play(Create(rl), run_time=2)
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05), FadeIn(side[:2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(opt), FadeIn(side[2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def kernels(self, k):
        Ps, err = np.log10(np.asarray(k["P"], float)), np.log10(np.asarray(k["err"]))
        g = axes([1, 4.5], [err.min() - 0.4, err.max() + 0.4], x_length=6.4, y_length=4.0, xlabel=r"random features $P$",
                 ylabel=r"mean $|z(x)^{\top}z(y) - k(x, y)|$", xticks=[1, 2, 3, 4], yticks=[], font_size=13,
                 log_x=True).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=COMPLEX) for x, y in zip(Ps, err)])
        guide = DashedLine(ax.c2p(Ps[0], err[0]), ax.c2p(Ps[-1], err[0] - 0.5 * (Ps[-1] - Ps[0])), color=HURDLE,
                           stroke_width=2)
        rows = VGroup(
            MathTex(r"z(x)^{\top}z(y) = \tfrac{2}{P}\textstyle\sum_{j \le P/2} \cos\big(w_j^{\top}(x - y)\big)",
                    font_size=26),
            MathTex(r"\xrightarrow{\ P \to \infty\ }\ \mathbb E\cos(w^{\top}\Delta) = e^{-\gamma^2|\Delta|^2/2}",
                    font_size=26),
            MathTex(r"\text{error} = O_p\big(P^{-1/2}\big)", font_size=26, color=HURDLE),
            wrapped_label(r"Rahimi and Recht (2007): Bochner's theorem writes the Gaussian kernel as the characteristic "
                          r"function of a normal; a sample average of cosines estimates it. So the random-feature ridge "
                          r"of Chapter 4 is, as $P \to \infty$, kernel ridge regression: Nagel's observation is a "
                          r"theorem. Mei and Montanari (2022) give its exact risk", 4.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        fit_right(rows)
        with self.voiceover(
            "One more theorem ties this to the critics. <bookmark mark='a'/> The inner product of two random-feature "
            "vectors is an average of cosines of random projections of the difference between the inputs. "
            "<bookmark mark='b'/> By Bochner's theorem its expectation is the Gaussian kernel, and by the law of large "
            "numbers the average converges to it, with an error that falls like one over the square root of the "
            "number of features: the gold line has slope minus a half, and the dots follow it. <bookmark mark='c'/> "
            "So as the features go to infinity, the random-feature ridge of Chapter 4 becomes kernel ridge "
            "regression. Nagel's reading in Chapter 5 is not a criticism of an implementation; it is a theorem about "
            "the limit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.2), Create(guide))
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: dense or sparse?", r"is return predictability many tiny signals (where large shrunk "
                          r"models win) or a few strong ones (where selection wins)? Giannone, Lenza and Primiceri (2021) "
                          r"find the data rarely tell; the answer decides the model class", width=12.4, font_size=18),
            desk_question(r"open: theory for markets", r"the theorems assume independent, identically distributed rows; "
                          r"returns are dependent, heavy-tailed and nonstationary, and the signal decays as it is "
                          r"traded. Exact risk under dependence and drift is largely unknown", width=12.4, font_size=18),
            desk_question(r"open: what deep networks add", r"gradient descent on a wide network behaves like a kernel "
                          r"method (the neural tangent kernel); whether finance's gains come from that kernel or from "
                          r"learned features is not settled", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three questions the literature has not settled. <bookmark mark='a'/> Is the predictability of returns "
            "dense, many tiny signals, where large shrunk models win, or sparse, a few strong ones, where selection "
            "wins? Giannone, Lenza and Primiceri found that in most economic data the evidence cannot tell, and the "
            "answer decides the model. <bookmark mark='b'/> The theorems assume independent, identically distributed "
            "observations. Returns are dependent, heavy-tailed and drifting, and their signal decays as it is traded; "
            "the exact risk under those conditions is largely unknown. <bookmark mark='c'/> And a very wide network "
            "trained by gradient descent behaves like a kernel method. Whether the gains of deep learning in finance "
            "come from that kernel, or from features the network genuinely learns, is open."
        ) as vo:
            for kk, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[kk], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"in the isotropic model with $r^2 = \sigma^2 = 1$, at what $\gamma > 1$ does the ridgeless risk "
                r"equal the risk of predicting zero? And what is the ridgeless risk at $\gamma = 1/2$?")
        with self.voiceover(
            "Pause and predict. In the isotropic model with signal and noise both equal to one, at what gamma above "
            "one does the ridgeless risk equal the risk of predicting zero? And what is it at gamma equals one half?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
