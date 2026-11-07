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
            cmath(r"0\le\ell\le1,\ \text{w.p. }1-\delta,\ \forall\rho", r":", r"\mathrm{kl}\big(R_n(\rho)\,\|\,R(\rho)\big) \le \frac{\mathrm{KL}(\rho\|\pi) + \log(2\sqrt n/\delta)}{n}", font_size=32),
            cmath(r"\text{weaker, \ simpler}", r":", r"R(\rho) \le R_n(\rho) + \sqrt{\frac{\mathrm{KL}(\rho\|\pi) + \log(2\sqrt n/\delta)}{2n}}", font_size=32),
        ]
        rows[2][-1].set_color(BOUNDC)
        whys = [why(r"no need to be true"), why(r"a Gibbs classifier"), why(r"Seeger; \ Maurer (2004)"), why(r"McAllester (1999)")]
        heading = label('Independent prior and bounded losses protect the Gibbs risk', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Take independent data, losses in zero to one, and a prior fixed independently of this sample. <bookmark mark='b'/> After seeing it, choose a posterior. The risk here is the Gibbs risk: average loss when a classifier is drawn from that posterior. It is not automatically the risk of a deterministic majority vote. <bookmark mark='c'/> With probability one minus delta, the binary KL bound holds simultaneously for all posteriors. <bookmark mark='d'/> Pinsker's inequality gives the simpler square-root version. These statements permit posterior and temperature selection on the same sample, because the event is already simultaneous."
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
        heading = label('A fixed prior and an exponential moment yield a simultaneous bound', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
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
            cmath(r"\text{so}", r":", r"\text{unbounded log loss needs a separate moment theorem}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BOUNDC)
        whys = [why(r"the variational objective"), why(r"Part 53's posterior"), why(r"the same objective"), why(r"two theories meet")]
        heading = label('The Gibbs variational identity is distinct from a generalization theorem', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A Gibbs posterior exactly minimizes a linear empirical-risk-plus-KL objective. It need not minimize the displayed nonlinear KL bound at a fixed temperature. Here lambda multiplies n times empirical risk; the preceding chart used lambda times empirical risk, so its temperature parameter is n times this one. <bookmark mark='b'/> Natural-log likelihood loss at lambda one yields the ordinary Bayesian posterior. <bookmark mark='c'/> The optimum variational objective equals minus log marginal likelihood. <bookmark mark='d'/> But log loss can be unbounded: applying a PAC-Bayes generalization theorem to evidence requires its own exponential-moment or model assumptions. Evidence alone is not a certificate from the bounded-loss theorem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def deep(self):
        rows = fit_rows(VGroup(
            label(r"PAC-Bayes bounds connect priors, flatness and generalization", font_size=36, color=WHITE),
            label(r"the prior may be anything chosen before the data, \ even learned on other data", font_size=26, color=CLASSC),
            label(r"flatness can preserve low loss; \ KL also depends on the prior", font_size=26, color=TESTC),
            label(r"Dziugaite \& Roy (2017): \ the first non-vacuous bounds for deep networks", font_size=26, color=GOODC),
            label(r"Catoni (2007): \ PAC-Bayes as a general theory of Gibbs estimators", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> PAC-Bayes is flexible because the reference prior need only be independent of the evaluated sample. <bookmark mark='b'/> A prior learned from separate data is allowed. Data-dependent choices on the same sample require a different bound or an explicit cost. <bookmark mark='c'/> Flatness helps find a spread-out posterior with low empirical loss, but does not by itself imply small KL: the reference prior and parameter scaling matter. <bookmark mark='d'/> Dziugaite and Roy constructed non-vacuous neural-network bounds by controlling both terms. <bookmark mark='e'/> Catoni developed related Gibbs estimators and bounds under explicit loss assumptions."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
