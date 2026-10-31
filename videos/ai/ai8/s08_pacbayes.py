from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, TEST, TRAIN, card_body, chapter, curve, load

PRIOR, POST = GREY_B, C.KL


class PACBayes(VoiceoverScene):
    def construct(self):
        chapter(self, 7, r"PAC-Bayes", r"A bound that says something about a network?",
                "Chapter seven. PAC-Bayes: a bound that says something about a network.")
        self.idea()
        self.derive()
        self.ours()

    # ------------------------------------------------------------------
    def idea(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.6, 1], x_length=6.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.3, 0.9, 0])
        pr = ax.plot(lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi) * 1.6, x_range=[-3, 3], color=PRIOR,
                     stroke_width=3)
        po = ax.plot(lambda x: math.exp(-(x - 1.2) ** 2 / (2 * 0.3 ** 2)) / (0.3 * math.sqrt(2 * math.pi)) * 0.55,
                     x_range=[-3, 3], color=POST, stroke_width=4)
        lp = label(r"prior $P$: \ chosen before the data", font_size=22, color=PRIOR).next_to(ax.c2p(-0.6, 0.62), UP, buff=0.1)
        lq = label(r"posterior $Q$: \ after", font_size=22, color=POST).next_to(ax.c2p(1.5, 0.75), UR, buff=0.05)
        sch = note(r"weights of the network, \ one direction \ (schematic)").next_to(ax, DOWN, buff=0.15)
        thm = theorem_card(r"PAC-Bayes",
                           card_body(r"for any prior $P$ fixed in advance, \ with probability $1 - \delta$, \ for "
                                     r"every posterior $Q$ at once:",
                                     r"\mathrm{kl}\big(\hat R(Q)\,\|\,R(Q)\big) \le \dfrac{\mathrm{KL}(Q\,\|\,P) + "
                                     r"\ln(2\sqrt n/\delta)}{n}",
                                     r"R(Q) \le \hat R(Q) + \sqrt{\dfrac{\mathrm{KL}(Q\,\|\,P) + \ln(2\sqrt n/\delta)}{2n}}",
                                     width=5.6, font_size=21),
                           who=r"D.~McAllester (1999); \ M.~Seeger (2002); \ A.~Maurer (2004)", width=6.4, font_size=21)
        thm.to_corner(UR, buff=0.3)
        defs = label(r"$R(Q)$: \ the error of a network drawn from $Q$; \\ kl: \ KL between two coins, \ "
                     r"$\mathrm{KL}(Q\|P)$: \ Part 1's divergence", font_size=21, color=GREY_A)
        defs.next_to(ax, DOWN, buff=0.7).align_to(ax, LEFT)
        hist = history_card(1999, r"D.~McAllester", r"\textit{PAC-Bayesian Model Averaging}: \ Bayesian priors, "
                            r"frequentist guarantees", width=5.6, font_size=18, color=HIST).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Counting doesn't work for networks, so change what is bounded. Instead of one network, take a "
            "distribution over networks, a cloud of weights, and bound the average error of a network drawn from "
            "it. <bookmark mark='a'/> Before seeing any data, choose a prior P over weights. After training, the "
            "posterior Q is wherever the data moved you. <bookmark mark='b'/> David McAllester's PAC-Bayes theorem, "
            "from 1999: with high probability, the posterior's true error is close to its training error, and how "
            "close depends on just one number, the KL divergence of Q from P, part one's measure of how many nats "
            "the data had to tell you. <bookmark mark='c'/> A posterior that's broad, close to the prior, costs few "
            "nats, whatever the number of weights."
        ) as vo:
            self.play(Create(ax), Create(pr), FadeIn(lp), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(po), FadeIn(lq))
            vo.wait_until("b")
            self.play(FadeIn(thm, shift=LEFT * 0.2), FadeIn(defs))
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\mathbb{E}_{Q}\, f", r"\le", r"\mathrm{KL}(Q\,\|\,P) + \ln \mathbb{E}_{P}\, e^{f}", font_size=32),
            cmath(r"\mathbb{E}_S\, \mathbb{E}_{P}\, e^{n\,\mathrm{kl}(\hat R(h)\|R(h))}", r"\le", r"2\sqrt n",
                  font_size=32),
            cmath(r"\ln \mathbb{E}_{P}\, e^{n\,\mathrm{kl}(\hat R(h)\|R(h))}", r"\le", r"\ln(2\sqrt n/\delta)",
                  font_size=32),
            cmath(r"n\,\mathrm{kl}\big(\hat R(Q)\,\|\,R(Q)\big)", r"\le",
                  r"\mathrm{KL}(Q\,\|\,P) + \ln(2\sqrt n/\delta)", font_size=32,
                  colors={r"\mathrm{KL}(Q\,\|\,P) + \ln(2\sqrt n/\delta)": BOUND}),
        ]
        whys = [why(r"change of measure \ (Donsker--Varadhan), \ for any $f$"),
                why(r"for each fixed $h$: \ the binomial tail \ (Maurer); \ swap $\mathbb{E}_S, \mathbb{E}_P$"),
                why(r"Markov: \ with probability $1 - \delta$ over $S$"),
                why(r"$f = n\,\mathrm{kl}$; \ kl is convex: \ Jensen")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.8, buff=0.55, edge=6.9)
        head = label(r"Why it holds, \ in four lines", font_size=30, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The proof is short. <bookmark mark='a'/> Start from a change of measure: an average under Q is at most "
            "the KL divergence from P plus the log of an exponential average under P. It's Gibbs' inequality from "
            "part one in disguise. <bookmark mark='b'/> For one fixed network, the chance that its training error "
            "is far from its true error is a binomial tail, so the exponential of n times their divergence averages "
            "to at most two root n. The prior was chosen without the data, so that holds averaged over P too. "
            "<bookmark mark='c'/> Markov's inequality turns the average into a statement that holds with "
            "probability one minus delta. <bookmark mark='d'/> Choose f to be n times the divergence, and use "
            "convexity: the bound. Nothing in it counts weights."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        p = load("pacbayes")
        cv = np.asarray(p["curve"])
        sg = np.asarray(p["sgd_curve"])
        steps = int(p["steps"])
        sm = np.convolve(cv[:, 3], np.ones(7) / 7, mode="same")
        sm[:3], sm[-3:] = cv[:3, 3], cv[-3:, 3]
        G = axes([0, steps], [0, 1.0], x_length=6.0, y_length=3.0, xticks=[0, steps // 2, steps],
                 xfmt=lambda v: fmt_int(v), yticks=[0, 0.5, 1.0], xlabel=r"steps of optimizing the bound",
                 center=(-3.2, -0.6, 0), font_size=18)
        ax = G.ax
        ob = curve(ax, cv[:, 0], np.clip(sm, 0, 1.0), BOUND, 3.5)
        sr = curve(ax, cv[:, 0], np.clip(cv[:, 4], 0, 1.0), TRAIN, 2.5)
        kmax = float(cv[:, 2].max()) * 1.15
        kx = axes([0, steps], [0, kmax], x_length=6.0, y_length=1.3, xticks=[], yticks=[0, round(kmax / 2, -1)],
                  center=(-3.2, 2.2, 0), font_size=16)
        kc = curve(kx.ax, cv[:, 0], cv[:, 2], POST, 3)
        kl_l = label(r"$\mathrm{KL}(Q\|P)$, \ nats", font_size=18, color=POST).next_to(kx, UP, buff=0.05).align_to(kx, LEFT)
        key = legend([(BOUND, r"the objective (smoothed): \ surrogate loss $+$ KL term"),
                      (TRAIN, r"error of one sampled network")], font_size=18).next_to(G, DOWN, buff=0.15).align_to(G, LEFT)
        kl0, kl1 = float(cv[0, 2]), float(p["kl"])
        net = label(rf"$70 \to {p['H']} \to 1$: \ ${fmt_int(p['params'])}$ weights, \ $n = {p['n']}$ pages",
                    font_size=24, color=WHITE).to_corner(UR, buff=0.35)
        recipe = VGroup(
            label(rf"prior: \ $\mathcal N(w_0, \lambda I)$, \ $w_0$ = the random initialization", font_size=20, color=PRIOR),
            label(rf"posterior: \ $\mathcal N(\mu, \mathrm{{diag}}\, s^2)$, \ from the trained network", font_size=20, color=POST),
            label(rf"each weight's noise $s$: \ median ${p['s_med']:.2f}$", font_size=20, color=POST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(net, DOWN, buff=0.2).align_to(net, LEFT)
        # the final account
        items = [(r"training error of $Q$ \ ($2{,}000$ networks)", p["e_hat"], TRAIN),
                 (r"its upper confidence limit", p["e_up"], TRAIN),
                 (rf"bound on $R(Q)$, \ $\mathrm{{KL}} = {p['kl']:.0f}$ nats \ (a coin: $50\%$)", p["bound"], BOUND),
                 (r"actual error of $Q$ on the $191$ test pages", p["test_Q"], TEST)]
        W = 3.6
        acct = VGroup()
        for txt, v, col in items:
            t = label(txt, font_size=19, color=col)
            bar = Rectangle(width=max(W * float(v), 0.02), height=0.22, stroke_width=0, fill_color=col, fill_opacity=0.85)
            val = MathTex(rf"{100 * float(v):.1f}\%", font_size=24, color=col)
            acct.add(VGroup(t, VGroup(bar, val)))
        for r_ in acct:
            r_[1][1].next_to(r_[1][0], RIGHT, buff=0.12)
            r_.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        acct.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(recipe, DOWN, buff=0.35).align_to(recipe, LEFT)
        base = acct[0][1][0].get_left()[0]
        for r_ in acct:
            r_[1].shift(RIGHT * (base - r_[1][0].get_left()[0]))
        nonvac = p["bound"] < 0.5
        hist = history_card(2017, r"G.~K.~Dziugaite \& D.~M.~Roy", r"the first non-vacuous bounds for deep networks: \ "
                            r"optimize the PAC-Bayes bound itself", width=5.0, font_size=17, color=HIST)
        hist.to_corner(DR, buff=0.2)
        verdict = (f"So the bound: the cloud's true error is at most {100 * p['bound']:.0f} percent. Loose next to the "
                   f"{100 * p['test_Q']:.1f} percent it actually gets on the test pages, and a bound under the theorem's assumptions for a "
                   "network with far more weights than data, where the VC bound is meaningless."
                   if nonvac else
                   f"The bound comes to {100 * p['bound']:.0f} percent, no better than a coin; the cloud actually "
                   f"errs on {100 * p['test_Q']:.1f} percent of the test pages.")
        with self.voiceover(
            f"Now our own. A network with {p['params']:,} weights, trained on {p['n']} pages: twenty times more "
            "weights than examples. Following Dziugaite and Roy's recipe from 2017, the prior is a Gaussian centred "
            "on its random starting weights. These book pages are correlated and their preprocessing is fitted: this illustrates the calculation, rather than certifying the theorem's IID risk. <bookmark mark='a'/> Train "
            f"briefly, then make the weights a cloud: a Gaussian around them, and optimize the bound itself, "
            f"for {steps:,} steps. Watch the KL: from {kl0:.0f} nats it settles near {kl1:.0f}, while the cloud "
            "widens wherever the weights don't matter. <bookmark mark='b'/> The final account. "
            f"Two thousand networks drawn from the cloud err on {100 * p['e_hat']:.1f} percent of the training "
            f"pages, at most {100 * p['e_up']:.1f} with confidence. The KL is {p['kl']:.0f} nats. "
            + "<bookmark mark='c'/> " + verdict
            + " <bookmark mark='d'/> The same idea, with networks compressed hard, gave the first non-vacuous bounds "
            "for language models in 2024, Lotfi and colleagues; counting tokens instead of documents later that year, "
            "for models as large as Llama 2 70B."
        ) as vo:
            self.play(FadeIn(net), FadeIn(recipe[:2]), FadeIn(G), FadeIn(kx), FadeIn(kl_l))
            vo.wait_until("a")
            self.play(Create(kc), Create(ob), Create(sr), FadeIn(key), FadeIn(recipe[2]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(acct[0]), FadeIn(acct[1]))
            vo.wait_until("c")
            self.play(FadeIn(acct[2]))
            self.play(FadeIn(acct[3]))
            vo.wait_until("d")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
