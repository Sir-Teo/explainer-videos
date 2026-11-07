from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Online(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.hedge()
        self.chart()
        self.bandits()
        self.bandit_chart()
        self.batch()
        self.mirror()

    def card(self):
        card = chapter_card(8, r"Online learning", r"Regret against an adversary", part=PART)
        with self.voiceover("Chapter eight. Online learning: regret against an adversary."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def game(self):
        rows = [
            cmath(r"t = 1, 2, \dots, T", r":", r"\text{predict, \ then see the loss } \ell_t \in [0, 1]^K", font_size=34),
            cmath(r"\text{no distribution}", r":", r"\text{the losses may be chosen by an adversary}", font_size=34),
            cmath(r"\text{regret}", r"=", r"\textstyle\sum_t \ell_t(\text{yours}) - \min_k \sum_t \ell_t(k)", font_size=36),
            cmath(r"\text{goal}", r":", r"\text{mixture regret}/T \to 0: \ \text{as good as the best expert in hindsight}", font_size=32),
        ]
        rows[2][-1].set_color(CLASSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"prediction with expert advice"), why(r"worst case, \ sequentially"), why(r"against a fixed comparator"), why(r"no-regret")]
        heading = label('Hedge controls mixture loss against a fixed expert comparator', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> In expert advice, choose a distribution over experts before observing the round's bounded loss vector. <bookmark mark='b'/> Losses may be adversarial. Our displayed Hedge guarantee uses the mixture's linear loss. If an expert is sampled instead, one needs a non-anticipating adversary for the corresponding expected-loss interpretation. <bookmark mark='c'/> Regret compares cumulative mixture loss with the best single expert in hindsight. <bookmark mark='d'/> The aim is sublinear regret, so average excess loss tends to zero. The adversary may use the past, but cannot see the current sampled action and then target that action under the standard randomized guarantee."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hedge(self):
        rows = [
            cmath(r"w_{t,k}", r"\propto", r"\exp\big(-\eta\textstyle\sum_{s<t}\ell_s(k)\big): \ \text{exponential weights}", font_size=34),
            cmath(r"\text{regret}", r"\le", r"\frac{\log K}{\eta} + \frac{\eta T}{8}", font_size=38),
            cmath(r"\eta = \sqrt{8\log K/T}", r"\Rightarrow", r"\text{regret} \le \sqrt{T\log K/2}", font_size=36),
            cmath(r"\text{minimax}", r":", r"\text{worst-case rate }\min\{T,\sqrt{T\log K}\}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Hedge (Freund \& Schapire 1997)"), why(r"a potential argument"), why(r"tuned"), why(r"Cesa-Bianchi \& Lugosi (2006)")]
        heading = label('Bounded losses yield a deterministic potential bound for the mixture', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Hedge, the exponential-weights algorithm of Freund and Schapire, weights each expert by e to "
            "the minus eta times its cumulative loss. <bookmark mark='b'/> A potential-function argument bounds its regret by "
            "log K over eta, plus eta T over eight. <bookmark mark='c'/> With eta tuned, the regret is at most the root of T "
            "log K over two: sublinear in T, and only logarithmic in the number of experts. <bookmark mark='d'/> No algorithm "
            "can do better against every sequence, up to constants, as Nicolò Cesa-Bianchi and Gábor Lugosi's book proves. "
            "And Hedge is AdaBoost's ancestor: boosting is Hedge played over training examples."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("online")
        lt = np.log10(d["ts"])
        A = axes([0.9, 3.8], [0, 105], x_length=7.4, y_length=4.4, xlabel=r"round $t$ \ (log scale)", ylabel=r"regret",
                 xticks=[1, 2, 3, np.log10(5000)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 25, 50, 75, 100], center=[-2.5, 0.2, 0])
        ax = A.ax
        cr = polyline(ax, lt, d["regret"], CLASSC, 4)
        cb = polyline(ax, lt, d["bound"], BOUNDC, 4)
        side = fit_rows(VGroup(
            label(rf"Hedge over $K = {d['K']}$ experts, \ $T = {d['T']:,}$ rounds", font_size=22),
            label(r"random losses; \ expert advantage 0.095 in expectation", font_size=22),
            label(rf"gold: \ regret, \ {d['final']:.1f} at the end", font_size=22, color=CLASSC),
            label(rf"purple: \ the bound $\log K/\eta + \eta t/8$, \ {d['final_bound']:.1f}", font_size=22, color=BOUNDC),
            label(rf"average regret per round: \ {d['final'] / d['T']:.4f}", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Hedge over fifty experts for five thousand rounds. <bookmark mark='b'/> The losses are random, with one expert slightly better on average. <bookmark mark='c'/> The regret, in gold, ends at {say(d['final'], 1)}. <bookmark mark='d'/> The bound, in purple, log K over eta plus eta t over eight, holds at every round and ends at {say(d['final_bound'], 1)}, with room to spare. <bookmark mark='e'/> Per round, the regret is {say(d['final'] / d['T'], 4)}: Hedge is almost exactly as good as the best expert, without knowing which one it is. This calculation uses the mixture loss, not a sampled action path."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bound exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cr), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bandits(self):
        rows = [
            cmath(r"\text{bandit feedback}", r":", r"\text{see only the loss of the arm you pulled}", font_size=34),
            cmath(r"\text{EXP3}", r":", r"\text{expected regret }O(\min\{T,\sqrt{TK\log K}\})", font_size=34),
            cmath(r"\text{stochastic arms}", r":", r"\text{fixed gaps: UCB1 }O(\textstyle\sum_{\Delta_k>0}\log T/\Delta_k)", font_size=34),
            cmath(r"\text{exploration}", r":", r"\text{the price of learning while acting}", font_size=34),
        ]
        rows[1][-1].set_color(CLASSC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"partial information"), why(r"Auer et al. (2002)"), why(r"Lai \& Robbins (1985)"), why(r"Part 58's adaptive trials")]
        heading = label('Missing feedback costs exploration; stochastic guarantees need a model', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Bandit feedback reveals only the selected arm's loss. <bookmark mark='b'/> For a non-anticipating adversary, EXP3 achieves expected regret of order root T K log K, capped by T. Minimax optimal algorithms remove the extra logarithm. <bookmark mark='c'/> For stationary independent stochastic arms, UCB1 has logarithmic instance-dependent regret when gaps are fixed. Lai and Robbins' lower bound has distribution-dependent KL constants, not simply inverse gaps in every model. <bookmark mark='d'/> It is an asymptotic statement for uniformly efficient algorithms, not a finite-round lower envelope for the plotted paths. Exploration trades immediate reward against information."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mirror(self):
        rows = [
            cmath(r"\text{online convex optimization}", r":", r"\text{convex losses; bounded domain and gradients}", font_size=34),
            cmath(r"\text{online gradient descent}", r":", r"x_{t+1} = \Pi(x_t - \eta\nabla f_t(x_t)): \ \text{regret } O(\sqrt T)", font_size=32),
            cmath(r"\text{strongly convex } f_t", r":", r"\text{regret } O(\log T)", font_size=36),
            cmath(r"\text{mirror descent}", r":", r"\text{Hedge and OGD are one algorithm, \ in different geometries}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"the general game"), why(r"Zinkevich (2003)"), why(r"Hazan et al. (2007)"), why(r"Nemirovski \& Yudin (1983)")]
        heading = label('Domain geometry, curvature and gradient bounds determine online regret', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Online convex optimization uses convex losses on a convex feasible set. <bookmark mark='b'/> With bounded diameter and gradient norms, projected gradient descent and a suitable step size give root T regret. Convexity alone is insufficient. <bookmark mark='c'/> Uniform strong convexity, bounded gradients and a decreasing step schedule can improve it to log T. <bookmark mark='d'/> Mirror descent changes the geometry: exponential weights uses negative entropy on the simplex, while ordinary projected gradient descent uses squared Euclidean distance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def batch(self):
        rows = [
            cmath(r"\text{online-to-batch}", r":", r"\text{i.i.d. data; convex averaging or randomized mixture}", font_size=32),
            cmath(r"E\,R(\bar h) - \min_k R(k)", r"\le", r"E[\text{regret}]/n", font_size=36),
            cmath(r"\text{Hedge}", r":", r"\sqrt{\log K/(2n)}: \ \text{the finite-class rate, \ again}", font_size=34),
            cmath(r"\text{online gradient descent}", r":", r"\text{regret } \sqrt T \ \Rightarrow \ \text{SGD's } 1/\sqrt n \text{ rate}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Cesa-Bianchi, \ Conconi \& Gentile (2004)"), why(r"regret controls risk"), why(r"chapter 1's bound"), why(r"Zinkevich (2003)")]
        heading = label('Convex averaging or a randomized mixture converts regret to risk', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> To convert online learning to a statistical result, feed independent observations sequentially, so each predictor is chosen before its next observation. <bookmark mark='b'/> For a convex loss, average iterates; for arbitrary expert classifiers, use their randomized mixture. Jensen's inequality or linearity then bounds expected excess risk by expected regret over n. <bookmark mark='c'/> Hedge recovers the finite-class square-root rate for the mixture, not automatically for a deterministic majority vote. <bookmark mark='d'/> With bounded domain and gradients, online gradient descent similarly gives a stochastic optimization rate of one over root n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bandit_chart(self):
        d = load("bandits")
        lt = np.log10(d["ts"])
        A = axes([1, np.log10(d["T"])], [0, 1300], x_length=7.4, y_length=4.4, xlabel=r"round $t$ \ (log scale)", ylabel=r"mean pseudo-regret, \ 10 runs",
                 xticks=[1, 2, 3, 4], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[0, 400, 800, 1200], center=[-2.5, 0.2, 0])
        ax = A.ax
        cu = polyline(ax, lt, d["ucb"], GOODC, 4)
        ce = polyline(ax, lt, d["exp3"], CLASSC, 4)
        cg = polyline(ax, lt, d["greedy"], BADC, 4)
        cl = DashedVMobject(polyline(ax, lt, d["lai"], BOUNDC, 3), num_dashes=40)
        mu = ", ".join(f"{m:g}" for m in d["mu"])
        side = fit_rows(VGroup(
            label(rf"five Bernoulli arms: \ {mu}", font_size=22),
            label(rf"red: \ $\varepsilon$-greedy, $\varepsilon = 0.1$: \ {d['greedy'][-1]:.0f}, \ linear", font_size=22, color=BADC),
            label(rf"gold: \ EXP3: \ {d['exp3'][-1]:.0f}, \ built for adversaries", font_size=22, color=CLASSC),
            label(rf"green: \ UCB1: \ {d['ucb'][-1]:.0f}, \ logarithmic", font_size=22, color=GOODC),
            label(rf"purple: \ Lai--Robbins asymptotic reference, \ {d['lai'][-1]:.0f}", font_size=22, color=BOUNDC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Five slot machines, with success rates from seven tenths down to three tenths, played for fifty thousand rounds, regret averaged over ten runs. <bookmark mark='b'/> Epsilon-greedy explores at random a tenth of the time, forever, so its regret grows linearly, to {say(d['greedy'][-1], 0)}; on the log scale it bends upward. <bookmark mark='c'/> EXP3, designed for an adversary, pays for its caution, ending at {say(d['exp3'][-1], 0)}. <bookmark mark='d'/> UCB1 explores only arms whose upper confidence bound is still competitive, and its regret grows like log T: a straight line on this scale, ending at {say(d['ucb'][-1], 0)}. <bookmark mark='e'/> The asymptotic Lai and Robbins reference, in purple, is also logarithmic; UCB1 matches its rate, with a larger constant. Suitable KL-UCB or Thompson-sampling algorithms achieve the asymptotic instance constant under additional assumptions; this line is not a finite-time lower bound."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ 10 runs")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cg), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ce), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cu), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cl), FadeIn(side[4]))
        self.clear_scene()
