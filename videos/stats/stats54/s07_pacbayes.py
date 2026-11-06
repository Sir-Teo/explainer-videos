from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class PACBayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.proof()
        self.chart()
        self.table()
        self.bayes()
        self.deep()

    def card(self):
        card = chapter_card(6, r"PAC-Bayes", r"Bounds for averaged rules, \ with a prior", lit=(1999,), part=PART)
        with self.voiceover("Chapter six. PAC-Bayes: bounds for averaged rules, with a prior."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\pi", r":", r"\text{a prior over rules, \ fixed before seeing the data}", font_size=34),
            cmath(r"\rho", r":", r"\text{any posterior, \ chosen after; \ } R(\rho) = E_{h \sim \rho} R(h)", font_size=34),
            cmath(r"\text{w.p. } 1 - \delta, \ \forall\rho", r":", r"\mathrm{kl}\big(R_n(\rho)\,\|\,R(\rho)\big) \le \frac{\mathrm{KL}(\rho\|\pi) + \log(2\sqrt n/\delta)}{n}", font_size=32),
            cmath(r"\text{weaker, \ simpler}", r":", r"R(\rho) \le R_n(\rho) + \sqrt{\frac{\mathrm{KL}(\rho\|\pi) + \log(2\sqrt n/\delta)}{2n}}", font_size=32),
        ]
        rows[2][-1].set_color(BOUNDC)
        whys = [why(r"no need to be true"), why(r"a Gibbs classifier"), why(r"Seeger; \ Maurer (2004)"), why(r"McAllester (1999)")]
        with self.voiceover(
            "<bookmark mark='a'/> PAC-Bayes, from David McAllester in 1999, mixes the two worlds. Fix a prior over rules "
            "before seeing the data; it need not be true, it is just a reference. <bookmark mark='b'/> After seeing the data, "
            "choose any posterior over rules, and consider its average risk. <bookmark mark='c'/> Then, with probability one "
            "minus delta, for every posterior simultaneously, the binary Kullback–Leibler divergence between its empirical and "
            "true average risk is at most the KL divergence from the posterior to the prior, plus a log term, over n. "
            "<bookmark mark='d'/> A weaker but simpler form: the true risk is at most the empirical risk plus the root of the "
            "same quantity over two n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"E_\rho[\phi] \le \mathrm{KL}(\rho\|\pi) + \log E_\pi[e^\phi]", r":", r"\text{the Donsker--Varadhan change of measure}", font_size=30),
            cmath(r"\phi = n\,\mathrm{kl}(R_n(h)\|R(h))", r":", r"E\,E_\pi e^\phi \le 2\sqrt n \ \text{ (Maurer)}", font_size=32),
            cmath(r"\text{Markov}", r":", r"\log E_\pi e^\phi \le \log(2\sqrt n/\delta) \ \text{ w.p. } 1 - \delta", font_size=34),
            cmath(r"\text{Jensen}", r":", r"\mathrm{kl} \text{ convex: \ } \mathrm{kl}(R_n(\rho)\|R(\rho)) \le E_\rho\,\mathrm{kl}", font_size=32),
        ]
        whys = [why(r"variational formula"), why(r"for one $h$"), why(r"the prior is fixed"), why(r"for the average")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof is four lines. The Donsker–Varadhan variational formula bounds any posterior "
            "expectation by the KL divergence plus the log of the prior expectation of an exponential. <bookmark mark='b'/> "
            "Take the exponent to be n times the binary KL between empirical and true risk: for each fixed rule its "
            "exponential moment is at most two root n, by Andreas Maurer's calculation. <bookmark mark='c'/> Since the prior "
            "does not depend on the data, Markov's inequality controls the prior average of that exponential. <bookmark "
            "mark='d'/> And the binary KL is convex, so Jensen moves the posterior average inside."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("pacbayes")
        lam = np.log10([r["lam"] for r in d["rows"]])
        A = axes([-0.1, 3.6], [0.1, 0.4], x_length=7.4, y_length=4.4, xlabel=r"inverse temperature $\lambda$ \ (log scale)", ylabel=r"risk",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[0.1, 0.2, 0.3, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax

        def line(key, c, w=4):
            v = [r[key] for r in d["rows"]]
            return VGroup(polyline(ax, lam, v, c, w), *[Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(lam, v)])

        ce, ct, cm, ck = line("emp", TRAINC), line("true", TESTC), line("mcallester", BOUNDC, 2.5), line("kl_bound", BOUNDC)
        un = DashedLine(ax.c2p(-0.1, d["union"]), ax.c2p(3.6, d["union"]), color=BADC, stroke_width=2.5)
        best = min(d["rows"], key=lambda r: r["kl_bound"])
        side = fit_rows(VGroup(
            label(rf"101 thresholds, \ uniform prior, \ $n = {d['n']}$, \ {100 * d['eta']:.0f}\% noise", font_size=22),
            label(r"Gibbs posterior $\rho \propto \pi\, e^{-\lambda R_n}$", font_size=22, color=CLASSC),
            label(r"teal: \ empirical risk; \ blue: \ true risk", font_size=22, color=TESTC),
            label(rf"purple: \ PAC-Bayes bounds; \ best {best['kl_bound']:.3f} at $\lambda = {best['lam']}$", font_size=22, color=BOUNDC),
            label(rf"red: \ ERM with the union bound, \ {d['union']:.3f}", font_size=22, color=BADC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test: a hundred and one threshold rules, a uniform prior over them, five hundred noisy "
            f"examples. <bookmark mark='b'/> The posterior is a Gibbs posterior, the prior reweighted by e to the minus lambda "
            f"times the empirical risk, Part fifty-three's object. <bookmark mark='c'/> As lambda grows, the posterior "
            f"concentrates on the empirically best rules: its empirical risk, in teal, and true risk, in blue, both fall. "
            f"<bookmark mark='d'/> The PAC-Bayes bounds in purple trade the falling empirical risk against the rising KL "
            f"divergence; the tighter one is lowest, {say(best['kl_bound'], 3)}, at lambda {best['lam']}. <bookmark "
            f"mark='e'/> The red line is the classical guarantee for ERM, a union bound over the hundred and one rules: "
            f"{say(d['union'], 3)}. The averaged rule's bound is a little better, and the true risk is "
            f"{say(best['true'], 3)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"one simulated sample; \ bounds exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ce), Create(ct), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cm), Create(ck), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(un), FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("pacbayes")
        rows = [[r"$\lambda$"] + [str(r["lam"]) for r in d["rows"]],
                [r"KL$(\rho\|\pi)$"] + [f"{r['kl']:.2f}" for r in d["rows"]],
                [r"$R_n(\rho)$"] + [f"{r['emp']:.3f}" for r in d["rows"]],
                [r"kl bound"] + [f"{r['kl_bound']:.3f}" for r in d["rows"]]]
        tab = table_rows(rows, font_size=26, col_buff=0.45, row_buff=0.4, colors=[GREY_B, CLASSC, TRAINC, BOUNDC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.9, 0])
        foot = label(r"KL never exceeds $\log 101 = 4.62$: \ the uniform prior's worst case is the union bound's $\log K$", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The trade-off in numbers. As lambda rises, the KL divergence from the uniform prior grows, "
            "the empirical risk falls, and the bound is smallest in between. <bookmark mark='b'/> The KL divergence can never "
            "exceed log a hundred and one, four point six two, reached when the posterior is a point mass: then PAC-Bayes "
            "reproduces the union bound's log K. Averaging over several good rules buys a smaller KL, and a better bound."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"one simulated sample")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bayes(self):
        rows = [
            cmath(r"\rho_\lambda \propto \pi\, e^{-\lambda n R_n}", r":", r"\text{minimizes } \lambda n R_n(\rho) + \mathrm{KL}(\rho\|\pi)", font_size=32),
            cmath(r"\text{log loss}, \ \lambda = 1", r":", r"\rho = \text{the Bayesian posterior}", font_size=34),
            cmath(r"\text{the bound}", r"\leftrightarrow", r"-\log(\text{marginal likelihood}): \ \text{Germain et al. (2016)}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{Bayesian model evidence is a PAC-Bayes certificate}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BOUNDC)
        whys = [why(r"the bound's optimizer"), why(r"Part 53's posterior"), why(r"the same objective"), why(r"two theories meet")]
        with self.voiceover(
            "<bookmark mark='a'/> The Gibbs posterior is not an arbitrary choice: it is exactly the posterior that minimizes the PAC-Bayes objective, lambda n times the empirical risk plus the KL divergence from the prior. <bookmark mark='b'/> With the log loss and lambda equal to one, it is the ordinary Bayesian posterior. <bookmark mark='c'/> Pascal Germain and colleagues showed in 2016 that the minimized bound is then essentially minus the log marginal likelihood. <bookmark mark='d'/> So the Bayesian model evidence of Part twenty-eight is a PAC-Bayes certificate: two theories that grew up apart meet in one formula."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def deep(self):
        rows = fit_rows(VGroup(
            label(r"why PAC-Bayes matters now:", font_size=28, color=GREY_A),
            label(r"the prior may be anything chosen before the data, \ even learned on other data", font_size=26, color=CLASSC),
            label(r"flat minima: \ a posterior spread around the weights, \ with small KL", font_size=26, color=TESTC),
            label(r"Dziugaite \& Roy (2017): \ the first non-vacuous bounds for deep networks", font_size=26, color=GOODC),
            label(r"Catoni (2007): \ PAC-Bayes as a general theory of Gibbs estimators", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why PAC-Bayes matters now. <bookmark mark='b'/> The prior can be anything fixed before the "
            "data are seen, even one learned on separate data, which makes the bounds remarkably flexible. <bookmark "
            "mark='c'/> For neural networks, a posterior spread around the trained weights has small KL if the training "
            "found a flat minimum, where perturbing the weights barely changes the loss. <bookmark mark='d'/> Gintare Karolina "
            "Dziugaite and Daniel Roy used this in 2017 to give the first non-vacuous generalization bounds for deep networks "
            "trained on real data. <bookmark mark='e'/> And Olivier Catoni's monograph of 2007 developed PAC-Bayes into a "
            "general theory of Gibbs estimators."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
