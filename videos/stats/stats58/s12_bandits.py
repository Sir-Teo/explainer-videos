from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Bandits(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eleven. Bandits and adaptive designs: choosing what to collect as the data arrive.",
                       11, r"Bandits and adaptive designs", r"Learn and earn at once", lit=(1933,))
        self.thompson()
        self.how()
        self.chart()
        self.lai_robbins()
        self.finite()
        self.policy_choice()
        self.tension()

    def thompson(self):
        heading = label('Posterior probability matching', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> William Thompson, in 1933, asked how to allocate patients between two treatments "
            "when each patient's outcome is seen before the next arrives. <bookmark mark='b'/> His answer: give "
            "each treatment with the posterior probability that it is the better one. <bookmark mark='c'/> Early "
            'on, when little is known, that is close to half and half; as evidence accumulates, the better '
            "treatment gets more patients. <bookmark mark='d'/> Forgotten for decades, Thompson sampling is now the "
            'workhorse of online experimentation, because it earns while it learns.'
        ),
            [(r"\text{Thompson (1933)}", r":", r"\text{allocate as the outcomes arrive}", 38),
             (r"P(\text{give } k)", r"=", r"P(\text{arm } k \text{ is best} \mid \text{data so far})", 38),
             (r"\text{early}", r":", r"\approx \text{balanced; \ later: \ mostly the better arm}", 38),
             (r"\text{today}", r":", r"\text{the workhorse of adaptive experiments}", 38)],
            [r"\emph{Biometrika} 25", r"probability matching", r"explore, \ then exploit", r"rediscovered"],
            colors=[(1, BANDITC)])

    def how(self):
        heading = label('Exact Thompson versus finite-MC matching', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Exact Bernoulli Thompson sampling keeps a Beta posterior for each arm. <bookmark "
            "mark='b'/> A single posterior draw per arm, followed by choosing the largest, samples exactly "
            'according to posterior winning probabilities. Our simulations use a distinct finite-Monte-Carlo '
            'probability-matching policy: draw a fixed batch of posterior samples, compute winning frequencies, '
            "then actually randomize the action using those frequencies. <bookmark mark='c'/> These frequencies are "
            'exact assignment probabilities conditional on the auxiliary draws, before the action and response. '
            "Update the chosen arm's posterior after observing its response. <bookmark mark='d'/> For inference "
            'examples, mix the frequencies with a uniform component so every arm has its stated minimum '
            'probability, and record them. Finite-Monte-Carlo matching is an approximation to exact Thompson '
            'sampling, not an automatic instance of its asymptotic theorem.'
        ),
            [(r"\text{posteriors}", r":", r"\mathrm{Beta}(1 + s_k, 1 + f_k) \text{ for each arm}", 38),
             (r"\text{each visitor}", r":", r"\text{draw } \tilde p_k; \ \text{show } \arg\max_k \tilde p_k", 38),
             (r"\text{update}", r":", r"s_k \text{ or } f_k \text{ of the arm shown}", 38),
             (r"\text{our simulation}", r":", r"e_t(k)=f+(1-Kf)\widehat p_t(k) \text{ before action}", 38)],
            [r"Part 15's conjugacy", r"one draw each", r"Bayes's rule", r"for chapter 12"],
            colors=[(3, BANDITC)])

    def chart(self):
        d = load("bandit")
        t = np.log10(d["t"])
        A = axes([0, math.log10(d["T"]) + 0.02], [0, 42], x_length=5.6, y_length=3.6, xlabel=r"visitors (log scale)",
                 ylabel=r"expected foregone conversions (pseudo-regret)", xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 10, 20, 40], center=[-3.4, 0.5, 0])
        B = axes([0, math.log10(d["T"]) + 0.02], [0, 1], x_length=5.6, y_length=3.6, xlabel=r"visitors (log scale)",
                 ylabel=r"share sent to the better design", xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 0.5, 1], center=[3.4, 0.5, 0])
        bal = polyline(A.ax, t, d["regret_balanced"], FIXEDC, 3.5)
        ts = polyline(A.ax, t, d["regret_ts"], BANDITC, 4)
        al = polyline(B.ax, t, d["alloc"], BANDITC, 4)
        half = DashedLine(B.ax.c2p(0, 0.5), B.ax.c2p(math.log10(d["T"]), 0.5), color=FIXEDC, stroke_width=2)
        m0, m1 = d["means"]
        foot = fit_rows(VGroup(
            label(rf"two page designs, \ conversion {100 * m0:.0f}\% and {100 * m1:.0f}\%; \ 60 runs of {d['T']:,} visitors", font_size=24, color=GREY_A),
            label(rf"red: \ a balanced test loses {d['final_bal']:.0f} conversions; \ purple: \ finite-MC matching loses {d['final_ts']:.0f}", font_size=24, color=BANDITC),
        ), 12.4, 0.22, [0, -2.75, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two page designs on the World's A/B platform, converting {100 * m0:.0f} and "
            f"{100 * m1:.0f} percent of visitors. <bookmark mark='b'/> A balanced test, half and half, loses a conversion for "
            f"every fifty visitors sent to the worse design, or every hundred visitors overall, in expectation: {d['final_bal']:.0f} by four thousand visitors. <bookmark "
            f"mark='c'/> finite-MC matching loses {d['final_ts']:.0f}, <bookmark mark='d'/> because by the end it sends "
            f"{100 * d['alloc'][-1]:.0f} percent of visitors to the better design. That is the earning. The cost, as chapter "
            f"twelve shows, is in what the data can then tell us."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), Create(half), FadeIn(simulated_tag(r"the World's A/B platform")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Create(bal), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ts), FadeIn(foot[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(al), run_time=2.0)
        self.clear_scene()

    def lai_robbins(self):
        d = load("bandit")
        c = d["lai_robbins_coef"]
        heading = label('The asymptotic regret lower bound', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> How few conversions can any policy lose? Tze Leung Lai and Herbert Robbins proved in 1985 "
            f"that the expected pseudo-regret of uniformly efficient policies across the Bernoulli model class grows at least like log T, <bookmark mark='b'/> with a constant equal "
            f"to the gap between the arms divided by their Kullback–Leibler divergence. <bookmark mark='c'/> Here, a gap of "
            f"two points and a divergence of about two thousandths give a constant of {c:.0f}: at least {c:.0f} log T "
            f"conversions, asymptotically. <bookmark mark='d'/> Thompson sampling attains that constant, as Emilie Kaufmann, "
            f"Nathaniel Korda and Rémi Munos showed in 2012, as does KL-UCB. Generic UCB bounds need not attain this sharp constant; our finite-Monte-Carlo approximation is not covered automatically.",
            [(r"\text{Lai--Robbins (1985)}", r":", r"\liminf_T \frac{\mathrm{Regret}_T}{\log T} \ge \sum_{k \ne *}\frac{\Delta_k}{\mathrm{KL}(p_k \,\|\, p_*)}", 34),
             (r"\Delta_k", r"=", r"p_* - p_k: \ \text{the gap}", 40),
             (r"\text{here}", r":", rf"\frac{{0.02}}{{\mathrm{{KL}}(0.10 \,\|\, 0.12)}} \approx {c:.0f}", 38),
             (r"\text{Thompson}", r":", r"\text{exact Bernoulli TS attains it; \ not a finite-MC theorem}", 36)],
            [r"the lower bound", r"how much each pull costs", r"a small gap is hard", r"KL-UCB; \ exact Bernoulli Thompson theorem"],
            colors=[(0, BANDITC), (3, CSC)])

    def finite(self):
        d = load("bandit")
        c = d["lai_robbins_coef"]
        T = d["T"]
        heading = label('An asymptotic bound is not a finite-horizon bound', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> A caution about asymptotics. At four thousand visitors, {c:.0f} log T is about {c * math.log(T):.0f} conversions, <bookmark mark='b'/> more than the balanced test's {d['final_bal']:.0f}, and larger than the simulated finite-Monte-Carlo regret. <bookmark mark='c'/> The bound is a statement about T going to infinity; it is not a finite-horizon lower bound, and this argument supplies no numerical crossover time. <bookmark mark='d'/> At realistic horizons, the right comparison is by simulation, as here, or by finite-time bounds.",
            [(r"\text{at } T = 4{,}000", r":", rf"{c:.0f}\log T \approx {c * math.log(T):.0f}", 40),
             (r"\text{actual}", r":", rf"\text{{balanced }} {d['final_bal']:.0f}, \ \text{{Thompson }} {d['final_ts']:.0f}", 40),
             (r"\text{the bound}", r":", r"\text{asymptotic: \ bites only for large } T", 38),
             (r"\text{in practice}", r":", r"\text{simulate, \ or use finite-time bounds}", 38)],
            [r"bigger than the truth", r"simulated", r"close arms", r"honest comparisons"],
            colors=[(0, FIXEDC), (1, BANDITC)])

    def policy_choice(self):
        heading = label('Allocation for final policy choice', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Some experiments aim to choose a policy after the trial rather than maximize "
            "rewards during it. <bookmark mark='b'/> Regret-oriented Thompson sampling still explores worse arms, "
            "but its allocation need not optimize final policy choice. <bookmark mark='c'/> Kasy and Sautmann "
            'propose exploration sampling, assigning in proportion to posterior best-arm probability times one '
            'minus that probability. Their asymptotic analysis concerns their policy-choice criterion and model. '
            "For two arms these products are equal, giving balanced allocation. <bookmark mark='d'/> They applied "
            'the method to six recruitment strategies for agricultural extension in India. This does not establish '
            'universal optimality for every best-arm identification loss or finite horizon.'
        ),
            [(r"\text{goal}", r":", r"\text{choose a policy afterwards, \ not earn now}", 38),
             (r"\text{Thompson}", r":", r"\text{too greedy for that}", 38),
             (r"\text{exploration sampling}", r":", r"q_k \propto p_k(1 - p_k), \ p_k = P(k \text{ best})", 38),
             (r"\text{result}", r":", r"\text{policy-choice asymptotics under stated model; \ field application}", 38)],
            [r"a different loss", r"exploits too soon", r"Kasy \& Sautmann (2021)", r"\emph{Econometrica} 89"],
            colors=[(2, BANDITC)])

    def tension(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Three goals pull against each other. <bookmark mark='b'/> Welfare during the "
            "experiment: send people to the better arm. <bookmark mark='c'/> Choosing the best arm: keep exploring "
            "the contenders. <bookmark mark='d'/> Inference: estimate every arm's effect with an honest interval, "
            "which needs every arm sampled enough. <bookmark mark='e'/> And adaptivity can invalidate unadjusted "
            "classical intervals, which is the next chapter's problem."
        ),
            [(r"three goals, \ pulling apart:", GREY_A),
             (r"welfare now: \ send people to the better arm", BANDITC),
             (r"the best choice later: \ keep exploring the contenders", WEALTHC),
             (r"inference: \ every arm sampled enough for an honest interval", CSC),
             (r"adaptivity can invalidate unadjusted intervals", FIXEDC)])
