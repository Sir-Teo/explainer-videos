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
        self.lad_voiceover(
            "<bookmark mark='a'/> William Thompson, in 1933, asked how to allocate patients between two treatments when "
            "each patient's outcome is seen before the next arrives. <bookmark mark='b'/> His answer: give each treatment with "
            "the posterior probability that it is the better one. <bookmark mark='c'/> Early on, when little is known, that "
            "is close to half and half; as evidence accumulates, the better treatment gets more patients. <bookmark mark='d'/> "
            "Forgotten for decades, Thompson sampling is now the workhorse of online experimentation, because it earns while "
            "it learns.",
            [(r"\text{Thompson (1933)}", r":", r"\text{allocate as the outcomes arrive}", 38),
             (r"P(\text{give } k)", r"=", r"P(\text{arm } k \text{ is best} \mid \text{data so far})", 38),
             (r"\text{early}", r":", r"\approx \text{balanced; \ later: \ mostly the better arm}", 38),
             (r"\text{today}", r":", r"\text{the workhorse of adaptive experiments}", 38)],
            [r"\emph{Biometrika} 25", r"probability matching", r"explore, \ then exploit", r"rediscovered"],
            colors=[(1, BANDITC)])

    def how(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In practice, for conversion rates: give each arm a Beta posterior. <bookmark mark='b'/> For "
            "each visitor, draw one sample from each posterior, and show the arm whose draw is largest. That assigns each arm "
            "with exactly its posterior probability of being best. <bookmark mark='c'/> Update the winner's posterior with "
            "the visitor's response. <bookmark mark='d'/> The assignment probabilities, which inference will need, are known "
            "at every step, and can be computed or floored at a minimum so that every arm keeps being seen.",
            [(r"\text{posteriors}", r":", r"\mathrm{Beta}(1 + s_k, 1 + f_k) \text{ for each arm}", 38),
             (r"\text{each visitor}", r":", r"\text{draw } \tilde p_k; \ \text{show } \arg\max_k \tilde p_k", 38),
             (r"\text{update}", r":", r"s_k \text{ or } f_k \text{ of the arm shown}", 38),
             (r"\text{record}", r":", r"e_t(k) = P(\text{arm } k \text{ shown at } t): \ \text{known}", 38)],
            [r"Part 15's conjugacy", r"one draw each", r"Bayes's rule", r"for chapter 12"],
            colors=[(3, BANDITC)])

    def chart(self):
        d = load("bandit")
        t = np.log10(d["t"])
        A = axes([0, math.log10(d["T"]) + 0.02], [0, 42], x_length=5.6, y_length=3.6, xlabel=r"visitors (log scale)",
                 ylabel=r"conversions lost to the worse design", xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 10, 20, 40], center=[-3.4, 0.5, 0])
        B = axes([0, math.log10(d["T"]) + 0.02], [0, 1], x_length=5.6, y_length=3.6, xlabel=r"visitors (log scale)",
                 ylabel=r"share sent to the better design", xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 0.5, 1], center=[3.4, 0.5, 0])
        bal = polyline(A.ax, t, d["regret_balanced"], FIXEDC, 3.5)
        ts = polyline(A.ax, t, d["regret_ts"], BANDITC, 4)
        al = polyline(B.ax, t, d["alloc"], BANDITC, 4)
        half = DashedLine(B.ax.c2p(0, 0.5), B.ax.c2p(math.log10(d["T"]), 0.5), color=FIXEDC, stroke_width=2)
        m0, m1 = d["means"]
        foot = fit_rows(VGroup(
            label(rf"two page designs, \ conversion {100 * m0:.0f}\% and {100 * m1:.0f}\%; \ 60 runs of {d['T']:,} visitors", font_size=24, color=GREY_A),
            label(rf"red: \ a balanced test loses {d['final_bal']:.0f} conversions; \ purple: \ Thompson sampling loses {d['final_ts']:.0f}", font_size=24, color=BANDITC),
        ), 12.4, 0.22, [0, -2.75, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two page designs on the World's A/B platform, converting {100 * m0:.0f} and "
            f"{100 * m1:.0f} percent of visitors. <bookmark mark='b'/> A balanced test, half and half, loses a conversion for "
            f"every hundred visitors it sends to the worse design: {d['final_bal']:.0f} by four thousand visitors. <bookmark "
            f"mark='c'/> Thompson sampling loses {d['final_ts']:.0f}, <bookmark mark='d'/> because by the end it sends "
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
        self.lad_voiceover(
            f"<bookmark mark='a'/> How few conversions can any policy lose? Tze Leung Lai and Herbert Robbins proved in 1985 "
            f"that the regret of every reasonable policy grows at least like log T, <bookmark mark='b'/> with a constant equal "
            f"to the gap between the arms divided by their Kullback–Leibler divergence. <bookmark mark='c'/> Here, a gap of "
            f"two points and a divergence of about two thousandths give a constant of {c:.0f}: at least {c:.0f} log T "
            f"conversions, asymptotically. <bookmark mark='d'/> Thompson sampling attains that constant, as Emilie Kaufmann, "
            f"Nathaniel Korda and Rémi Munos showed in 2012, and as Part fifty-four's UCB does too.",
            [(r"\text{Lai--Robbins (1985)}", r":", r"\liminf_T \frac{\mathrm{Regret}_T}{\log T} \ge \sum_{k \ne *}\frac{\Delta_k}{\mathrm{KL}(p_k \,\|\, p_*)}", 34),
             (r"\Delta_k", r"=", r"p_* - p_k: \ \text{the gap}", 40),
             (r"\text{here}", r":", rf"\frac{{0.02}}{{\mathrm{{KL}}(0.10 \,\|\, 0.12)}} \approx {c:.0f}", 38),
             (r"\text{Thompson}", r":", r"\text{attains it \ (Kaufmann, \ Korda \& Munos 2012)}", 36)],
            [r"the lower bound", r"how much each pull costs", r"a small gap is hard", r"and Part 54's UCB"],
            colors=[(0, BANDITC), (3, CSC)])

    def finite(self):
        d = load("bandit")
        c = d["lai_robbins_coef"]
        T = d["T"]
        self.lad_voiceover(
            f"<bookmark mark='a'/> A caution about asymptotics. At four thousand visitors, {c:.0f} log T is about "
            f"{c * math.log(T):.0f} conversions, <bookmark mark='b'/> more than the balanced test's {d['final_bal']:.0f}, and five "
            f"times what Thompson sampling actually lost. <bookmark mark='c'/> The bound is a statement about T going to "
            f"infinity; with arms this close, it only bites after tens of thousands of visitors. <bookmark mark='d'/> At "
            f"realistic horizons, the right comparison is by simulation, as here, or by finite-time bounds.",
            [(r"\text{at } T = 4{,}000", r":", rf"{c:.0f}\log T \approx {c * math.log(T):.0f}", 40),
             (r"\text{actual}", r":", rf"\text{{balanced }} {d['final_bal']:.0f}, \ \text{{Thompson }} {d['final_ts']:.0f}", 40),
             (r"\text{the bound}", r":", r"\text{asymptotic: \ bites only for large } T", 38),
             (r"\text{in practice}", r":", r"\text{simulate, \ or use finite-time bounds}", 38)],
            [r"bigger than the truth", r"simulated", r"close arms", r"honest comparisons"],
            colors=[(0, FIXEDC), (1, BANDITC)])

    def policy_choice(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> But an experiment's purpose is often not to earn during the experiment; it is to choose a "
            "policy afterwards. <bookmark mark='b'/> Then Thompson sampling is too greedy: it stops learning about arms that "
            "look worse, and the final choice suffers. <bookmark mark='c'/> Maximilian Kasy and Anja Sautmann's exploration "
            "sampling, in 2021, assigns in proportion to the posterior probability of being best times one minus it, "
            "spreading effort among the close contenders. <bookmark mark='d'/> They prove it asymptotically optimal for "
            "picking the best policy, and used it to choose among recruitment strategies for an agricultural extension "
            "service in India.",
            [(r"\text{goal}", r":", r"\text{choose a policy afterwards, \ not earn now}", 38),
             (r"\text{Thompson}", r":", r"\text{too greedy for that}", 38),
             (r"\text{exploration sampling}", r":", r"q_k \propto p_k(1 - p_k), \ p_k = P(k \text{ best})", 38),
             (r"\text{result}", r":", r"\text{optimal for policy choice; \ used in the field}", 38)],
            [r"a different loss", r"exploits too soon", r"Kasy \& Sautmann (2021)", r"\emph{Econometrica} 89"],
            colors=[(2, BANDITC)])

    def tension(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Three goals pull against each other. <bookmark mark='b'/> Welfare during the experiment: "
            "send people to the better arm. <bookmark mark='c'/> Choosing the best arm: keep exploring the contenders. "
            "<bookmark mark='d'/> Inference: estimate every arm's effect with an honest interval, which needs every arm "
            "sampled enough. <bookmark mark='e'/> And adaptivity itself breaks the classical intervals, which is the next "
            "chapter's problem.",
            [(r"three goals, \ pulling apart:", GREY_A),
             (r"welfare now: \ send people to the better arm", BANDITC),
             (r"the best choice later: \ keep exploring the contenders", WEALTHC),
             (r"inference: \ every arm sampled enough for an honest interval", CSC),
             (r"and adaptivity breaks the classical intervals", FIXEDC)])
