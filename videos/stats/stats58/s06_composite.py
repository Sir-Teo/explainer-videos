from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Composite(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Composite nulls: when the null hypothesis is a family, how can a bet be fair "
                       "against all of it?", 5, r"Composite nulls", r"Fair against a whole family", lit=(2020, 2024))
        self.problem()
        self.universal()
        self.why_valid()
        self.table()
        self.price()
        self.grow()
        self.ripr()
        self.tests_compare()

    def problem(self):
        heading = label('Fairness against every null member', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> So far the null was simple: one distribution. Most nulls are composite: a normal "
            "mean of zero with unknown variance, or independence of two variables. <bookmark mark='b'/> An e-value "
            'must then have expectation at most one under every distribution in the null at once. <bookmark '
            "mark='c'/> A likelihood ratio against one member of the null is not enough: under another member it "
            "can have expectation far above one. <bookmark mark='d'/> Two answers have emerged: universal "
            'inference, valid with correct split likelihoods, and the growth-optimal e-values of safe testing, '
            'which are efficient.'
        ),
            [(r"\text{composite}", r":", r"H_0 = \{P_\theta: \theta \in \Theta_0\}", 40),
             (r"\text{need}", r":", r"E_{P}[E] \le 1 \text{ for every } P \in H_0", 40),
             (r"\text{a single LR}", r":", r"\text{fair against one member only}", 38),
             (r"\text{answers}", r":", r"\text{universal inference; \ GROW e-values}", 38)],
            [r"$\sigma$ unknown, \ independence", r"every member at once", r"the difficulty", r"chapters ahead"],
            colors=[(1, WEALTHC)])

    def universal(self):
        heading = label('Independent split likelihood ratios', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Universal inference begins with independent training and evaluation halves from a "
            'correctly specified IID model. It needs normalized likelihoods, but not a regular asymptotic '
            "approximation. <bookmark mark='b'/> Fit any proper alternative density on the training half. <bookmark "
            "mark='c'/> On the independent evaluation half, divide its likelihood by the supremum of the null "
            'likelihood. That denominator must be the true supremum, or a certified upper bound; a failed '
            "optimization can invalidate the guarantee. <bookmark mark='d'/> The result is an e-value for every "
            'null member. This is a fixed-sample construction; repeatedly reusing it at new sample sizes does not '
            'automatically produce an e-process.'
        ),
            [(r"\text{split}", r":", r"D_0, \ D_1", 40),
             (r"\text{on } D_0", r":", r"\hat\theta_1 = \text{any estimate}", 40),
             (r"\text{on } D_1", r":", r"U = \frac{\prod_{D_1} p_{\hat\theta_1}(x)}{\sup_{\theta \in \Theta_0}\prod_{D_1} p_\theta(x)}", 38),
             (r"\text{then}", r":", r"E_{P}[U] \le 1 \text{ for every } P \in H_0", 40)],
            [r"Wasserman, \ Ramdas \& Balakrishnan (2020)", r"anything: \ MLE, \ Bayes, \ a guess", r"the split LRT", r"correct independent likelihood model"],
            colors=[(2, WEALTHC), (3, CSC)])

    def why_valid(self):
        heading = label('Why the split ratio is an e-value', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Fix a true null member. The null likelihood supremum is at least its likelihood "
            "on the evaluation half. <bookmark mark='b'/> The split ratio is therefore bounded above by a "
            "likelihood ratio against that true distribution. <bookmark mark='c'/> Conditional on the independent "
            'training half, the fitted alternative is fixed. Its likelihood ratio has expectation at most one, with '
            'equality when the alternative is absolutely continuous with respect to the true distribution. '
            "<bookmark mark='d'/> Taking expectations proves the e-value guarantee. Averaging a fixed collection of "
            'valid split e-values preserves validity and reduces dependence on one random split, without '
            'necessarily removing all split randomness.'
        ),
            [(r"\sup_{\Theta_0} L_1(\theta)", r"\ge", r"L_1(\theta^*)", 40),
             (r"U", r"\le", r"L_1(\hat\theta_1)/L_1(\theta^*)", 40),
             (r"E_{\theta^*}\big[L_1(\hat\theta_1)/L_1(\theta^*) \mid D_0\big]", r"\le", r"1", 38),
             (r"\Rightarrow", r"\;", r"E_{\theta^*}[U] \le 1 \qquad \blacksquare", 40)],
            [r"$\theta^*$ is in the null", r"a bigger denominator", r"$\hat\theta_1$ fixed given $D_0$", r"average over splits too"],
            colors=[(3, CSC)])

    def table(self):
        d = load("ui")
        hdr = [r"true mean $\mu$", r"$t$-test \ (5\%, \ fixed $n$)", r"universal, \ reject if $U \ge 20$", r"median $U$"]
        body = [[f"{r['mu']:g}", f"{100 * r['t_reject']:.1f}\\%", f"{100 * r['ui_reject']:.1f}\\%", f"{r['median_e']:.2f}" if r["median_e"] < 100 else f"{r['median_e']:.0f}"]
                for r in d["rows"]]
        cols = [GREY_B] + [WHITE] * len(body)
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.25, colors=cols).move_to([0, 0.5, 0])
        r0, r5 = d["rows"][0], d["rows"][2]
        foot = fit_rows(VGroup(
            label(rf"$H_0$: \ $\mu = 0$, \ $\sigma$ unknown; \ $n = {d['n']}$; \ {d['reps']:,} data sets per row", font_size=24, color=GREY_A),
            label(rf"universal inference: \ valid, \ size {100 * r0['ui_reject']:.1f}\%; \ but at $\mu = 0.5$ power {100 * r5['ui_reject']:.0f}\% \ against {100 * r5['t_reject']:.0f}\%", font_size=24, color=WEALTHC),
        ), 12.4, 0.22, [0, -2.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Universal inference against the t-test, for a normal mean of zero with unknown variance, "
            f"forty observations. <bookmark mark='b'/> Under the null, the t-test rejects {100 * r0['t_reject']:.1f} percent of "
            f"the time and universal inference {100 * r0['ui_reject']:.1f} percent: both valid, the second very conservative. "
            f"<bookmark mark='c'/> At a mean of a half, the t-test's power is {100 * r5['t_reject']:.0f} percent, universal "
            f"inference's only {100 * r5['ui_reject']:.0f}. <bookmark mark='d'/> Validity came free; efficiency did not. The "
            f"split throws away half the data for fitting, and the split likelihood ratio and Markov threshold are conservative in this example; both tests target five-percent size."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(tab[3], color=WEALTHC))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def price(self):
        heading = label('Validity and the efficiency of this split test', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The price can be read off. Universal inference's rejection threshold corresponds "
            'roughly to a likelihood-ratio statistic of two log of one over alpha, computed on half the data. '
            "<bookmark mark='b'/> In regular problems, where Wilks's chi-squared threshold applies, that makes it "
            "clearly less powerful, as the table showed. <bookmark mark='c'/> It is a price worth paying where "
            'Wilks fails: mixtures, shape constraints such as log-concavity, and boundaries, where no classical '
            "test has a known null distribution. <bookmark mark='d'/> Robin Dunn and colleagues, for example, built "
            'from it a practical test of log-concavity.'
        ),
            [(r"\text{threshold}", r":", r"2\log U \ge 2\log(1/\alpha) \text{ on half the data}", 38),
             (r"\text{regular problems}", r":", r"\text{less power than the classical test}", 38),
             (r"\text{where it shines}", r":", r"\text{mixtures, \ shape constraints, \ boundaries}", 38),
             (r"\text{example}", r":", r"\text{a valid test of log-concavity}", 38)],
            [r"compare $\chi^2_{1, 0.95} = 3.84$", r"for $\sigma$ unknown", r"where Wilks fails", r"Dunn and colleagues"],
            colors=[(2, CSC)])

    def grow(self):
        heading = label('Growth optimality for a specified alternative', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> For a specified alternative Q, maximize expected log payoff among all e-values "
            'valid for the null family. This is the simple-alternative version of the growth-optimal criterion; a '
            "composite alternative requires a separate worst-case optimization. <bookmark mark='b'/> Under suitable "
            'domination, existence and integrability conditions, the solution is q divided by its reverse '
            'information projection onto the closed convex null family. The projection may be a mixture, rather '
            "than a member of the original null. <bookmark mark='c'/> For suitable invariant problems, including a "
            'scale-invariant t-test, the maximal-invariant likelihood ratio has an optimality result. <bookmark '
            "mark='d'/> Its stopping guarantee is relative to the maximal-invariant filtration. An arbitrary "
            'raw-data stopping rule can invalidate its stopped e-value; the filtration is part of the theorem.'
        ),
            [(r"\text{GROW}", r":", r"\max_E E_Q[\log E] \text{ over valid } E \quad (Q\text{ fixed})", 36),
             (r"\text{answer}", r":", r"E^* = q / p_{\mathrm{RIPr}}, \ \ p_{\mathrm{RIPr}} = \arg\min_{p \in \mathrm{conv}(H_0)} \mathrm{KL}(q \,\|\, p)", 34),
             (r"\text{t-test}", r":", r"\text{stopping within the maximal-invariant filtration}", 38),
             (r"\text{result}", r":", r"\text{validity and optimality under the theorem assumptions}", 38)],
            [r"Gr\"unwald, \ de Heide \& Koolen (2024)", r"the reverse information projection", r"P\'erez-Ortiz et al. (2024)", r"efficient"],
            colors=[(1, WEALTHC), (3, CSC)])

    def ripr(self):
        heading = label('Projection conditions imply fairness', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Suppose the reverse information projection exists as a dominating density and the "
            "differentiation conditions hold. <bookmark mark='b'/> Perturb that minimizing density toward any "
            'density in the convex null family. The nonnegative directional derivative of the Kullback-Leibler '
            'objective says that the null expectation of q divided by the projection is at most one. <bookmark '
            "mark='c'/> This is precisely the e-value requirement for every original null member. <bookmark "
            "mark='d'/> The least favourable comparison can lie in the convex hull rather than the original family. "
            'Without an attained projection, a generalized projection theorem is needed; the displayed ratio is not '
            'an unconditional existence claim.'
        ),
            [(r"\text{why fair}", r":", r"\text{the projection's first-order condition}", 38),
             (r"E_P\big[q/p_{\mathrm{RIPr}}\big]", r"\le", r"1 \text{ for all } P \in \mathrm{conv}(H_0)", 38),
             (r"=", r"\;", r"\text{validity for the whole null}", 38),
             (r"\text{reading}", r":", r"\text{a likelihood ratio against the least favourable null}", 36)],
            [r"convex duality", r"Gr\"unwald, \ de Heide \& Koolen", r"the requirement, \ met", r"Part 50's idea"],
            colors=[(1, CSC), (3, WEALTHC)])

    def tests_compare(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Composite nulls require a bet fair against the whole family. <bookmark mark='b'/> "
            'Split likelihood ratios give fixed-sample e-values under correct independent evaluation likelihoods, '
            "often conservatively. <bookmark mark='c'/> Growth-optimal constructions can exploit structure, but "
            "their existence, optimality and filtration assumptions matter. <bookmark mark='d'/> Mixtures preserve "
            'a common sequential validity guarantee, and predictable plug-in alternatives work against a simple '
            "conditional null. Neither device alone solves an arbitrary composite null. <bookmark mark='e'/> Choose "
            'a construction whose assumptions and stopping information match the scientific experiment.'
        ),
            [(r"for composite nulls:", GREY_A),
             (r"universal inference: \ independent split, \ correct likelihood model; \ often conservative", WEALTHC),
             (r"GROW e-values: \ optimal growth; \ explicit for $t$-tests, \ $2 \times 2$ tables, \ exponential families", CSC),
             (r"sequential extensions need validity in the stated filtration", SPRTC),
             (r"the choice: \ how much structure can be computed with", GREY_A)])
