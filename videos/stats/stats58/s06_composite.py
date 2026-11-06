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
        self.lad_voiceover(
            "<bookmark mark='a'/> So far the null was simple: one distribution. Most nulls are composite: a normal mean of "
            "zero with unknown variance, or independence of two variables. <bookmark mark='b'/> An e-value must then have "
            "expectation at most one under every distribution in the null at once. <bookmark mark='c'/> A likelihood ratio "
            "against one member of the null is not enough: under another member it can have expectation far above one. "
            "<bookmark mark='d'/> Two answers have emerged: universal inference, which is simple and always valid, and the "
            "growth-optimal e-values of safe testing, which are efficient.",
            [(r"\text{composite}", r":", r"H_0 = \{P_\theta: \theta \in \Theta_0\}", 40),
             (r"\text{need}", r":", r"E_{P}[E] \le 1 \text{ for every } P \in H_0", 40),
             (r"\text{a single LR}", r":", r"\text{fair against one member only}", 38),
             (r"\text{answers}", r":", r"\text{universal inference; \ GROW e-values}", 38)],
            [r"$\sigma$ unknown, \ independence", r"every member at once", r"the difficulty", r"chapters ahead"],
            colors=[(1, WEALTHC)])

    def universal(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Larry Wasserman, Aaditya Ramdas and Sivaraman Balakrishnan's universal inference, from "
            "2020. Split the data in two halves. <bookmark mark='b'/> On the first half, fit any estimate of the alternative "
            "you like, theta hat one. <bookmark mark='c'/> On the second half, compute the likelihood at theta hat one, "
            "divided by the likelihood maximized over the null. <bookmark mark='d'/> That ratio is an e-value for the whole "
            "composite null, with no regularity conditions at all: no smoothness, no asymptotics, no boundary problems.",
            [(r"\text{split}", r":", r"D_0, \ D_1", 40),
             (r"\text{on } D_0", r":", r"\hat\theta_1 = \text{any estimate}", 40),
             (r"\text{on } D_1", r":", r"U = \frac{\prod_{D_1} p_{\hat\theta_1}(x)}{\sup_{\theta \in \Theta_0}\prod_{D_1} p_\theta(x)}", 38),
             (r"\text{then}", r":", r"E_{P}[U] \le 1 \text{ for every } P \in H_0", 40)],
            [r"Wasserman, \ Ramdas \& Balakrishnan (2020)", r"anything: \ MLE, \ Bayes, \ a guess", r"the split LRT", r"no regularity"],
            colors=[(2, WEALTHC), (3, CSC)])

    def why_valid(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why? Fix a true member theta star of the null. The denominator, the maximum over the null, "
            "is at least the likelihood at theta star. <bookmark mark='b'/> So U is at most the likelihood ratio of theta hat "
            "one against theta star on the second half. <bookmark mark='c'/> Theta hat one was fitted on the other half, so "
            "it is fixed given the first half, and that likelihood ratio has expectation exactly one under theta star. "
            "<bookmark mark='d'/> Hence the expectation of U is at most one: three lines, no conditions. Repeating the split "
            "and averaging the e-values keeps validity and removes the randomness of one split.",
            [(r"\sup_{\Theta_0} L_1(\theta)", r"\ge", r"L_1(\theta^*)", 40),
             (r"U", r"\le", r"L_1(\hat\theta_1)/L_1(\theta^*)", 40),
             (r"E_{\theta^*}\big[L_1(\hat\theta_1)/L_1(\theta^*) \mid D_0\big]", r"=", r"1", 38),
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
            f"split throws away half the data for fitting, and the threshold twenty is stricter than a p-value of five percent."
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
        self.lad_voiceover(
            "<bookmark mark='a'/> The price can be read off. Universal inference's rejection threshold corresponds roughly to "
            "a likelihood-ratio statistic of two log of one over alpha, computed on half the data. <bookmark mark='b'/> In "
            "regular problems, where Wilks's chi-squared threshold applies, that makes it clearly less powerful, as the table "
            "showed. <bookmark mark='c'/> It is a price worth paying where Wilks fails: mixtures, shape constraints such as "
            "log-concavity, and boundaries, where no classical test has a known null distribution. <bookmark mark='d'/> Robin "
            "Dunn and colleagues, for example, built from it a practical test of log-concavity.",
            [(r"\text{threshold}", r":", r"2\log U \ge 2\log(1/\alpha) \text{ on half the data}", 38),
             (r"\text{regular problems}", r":", r"\text{less power than the classical test}", 38),
             (r"\text{where it shines}", r":", r"\text{mixtures, \ shape constraints, \ boundaries}", 38),
             (r"\text{example}", r":", r"\text{a valid test of log-concavity}", 38)],
            [r"compare $\chi^2_{1, 0.95} = 3.84$", r"for $\sigma$ unknown", r"where Wilks fails", r"Dunn and colleagues"],
            colors=[(2, CSC)])

    def grow(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Peter Grünwald, Rianne de Heide and Wouter Koolen asked for the best e-value instead. For "
            "a given alternative Q, choose the e-value that maximizes the expected log under Q, among all e-values valid for "
            "the whole null: the GROW criterion, growth-rate optimal in the worst case. <bookmark mark='b'/> Its answer is a "
            "likelihood ratio, Q over a special mixture of the null: the reverse information projection of Q onto the null's "
            "convex hull, the null mixture closest to Q in Kullback–Leibler divergence. <bookmark mark='c'/> For the t-test's "
            "null, group invariance makes the optimal e-value explicit: an anytime-valid t-test. <bookmark mark='d'/> Validity is exact, and power is "
            "near the classical test's.",
            [(r"\text{GROW}", r":", r"\max_E \min_{Q \in H_1} E_Q[\log E] \text{ over valid } E", 36),
             (r"\text{answer}", r":", r"E^* = q / p_{\mathrm{RIPr}}, \ \ p_{\mathrm{RIPr}} = \arg\min_{p \in \mathrm{conv}(H_0)} \mathrm{KL}(q \,\|\, p)", 34),
             (r"\text{t-test}", r":", r"\text{by invariance: \ an anytime-valid } t\text{-test}", 38),
             (r"\text{result}", r":", r"\text{exact validity, \ near-classical power}", 38)],
            [r"Gr\"unwald, \ de Heide \& Koolen (2024)", r"the reverse information projection", r"P\'erez-Ortiz et al. (2024)", r"efficient"],
            colors=[(1, WEALTHC), (3, CSC)])

    def ripr(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why does the projection make the bet fair? <bookmark mark='b'/> The optimality condition "
            "of the projection says that, for every distribution P in the null's convex hull, the expectation under P of q "
            "over the projection is at most one. <bookmark mark='c'/> That is exactly validity for the whole null. <bookmark "
            "mark='d'/> So the growth-optimal e-value is a likelihood ratio after all, against the one member of the null "
            "that the alternative finds hardest to tell apart from itself: Part fifty's least favourable distribution, in "
            "the language of bets.",
            [(r"\text{why fair}", r":", r"\text{the projection's first-order condition}", 38),
             (r"E_P\big[q/p_{\mathrm{RIPr}}\big]", r"\le", r"1 \text{ for all } P \in \mathrm{conv}(H_0)", 38),
             (r"=", r"\;", r"\text{validity for the whole null}", 38),
             (r"\text{reading}", r":", r"\text{a likelihood ratio against the least favourable null}", 36)],
            [r"convex duality", r"Gr\"unwald, \ de Heide \& Koolen", r"the requirement, \ met", r"Part 50's idea"],
            colors=[(1, CSC), (3, WEALTHC)])

    def tests_compare(self):
        self.list_voiceover(
            "<bookmark mark='a'/> A summary for composite nulls. <bookmark mark='b'/> Universal inference: one split, any "
            "model, valid always, often conservative. <bookmark mark='c'/> GROW e-values: optimal growth, exact validity, "
            "explicit for the t-test, two-by-two tables and exponential families, harder elsewhere. <bookmark mark='d'/> "
            "Mixtures and plug-in alternatives give e-processes, valid at every stopping time, for both. <bookmark mark='e'/> "
            "Which to use is a question of how much of the problem's structure one can compute with.",
            [(r"for composite nulls:", GREY_A),
             (r"universal inference: \ one split, \ any model, \ always valid, \ often conservative", WEALTHC),
             (r"GROW e-values: \ optimal growth; \ explicit for $t$-tests, \ $2 \times 2$ tables, \ exponential families", CSC),
             (r"mixtures or plug-in bets: \ e-processes, \ valid at every stopping time", SPRTC),
             (r"the choice: \ how much structure can be computed with", GREY_A)])
