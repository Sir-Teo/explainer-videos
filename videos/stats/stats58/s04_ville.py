from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Ville(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. Test martingales and Ville's inequality: one line of 1939 that makes peeking "
                       "safe.", 3, r"Test martingales and Ville", r"Peeking, made safe", lit=(1939,))
        self.definition()
        self.inequality()
        self.proof()
        self.peek_chart()
        self.paths()
        self.sprt_again()
        self.stopping()
        self.anytime_p()

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A test martingale for a null hypothesis is a process M t with three properties. It starts "
            "at one. <bookmark mark='b'/> It is never negative. <bookmark mark='c'/> And under the null, it is a martingale: "
            "its expected next value, given everything so far, is its current value. <bookmark mark='d'/> The likelihood "
            "ratio of any alternative against a simple null is one: Part forty-four met it as the wealth of a gambler betting "
            "against the null at fair odds.",
            [(r"M_0", r"=", r"1", 40),
             (r"M_t", r"\ge", r"0", 40),
             (r"E_{H_0}[M_{t+1} \mid \mathcal F_t]", r"=", r"M_t \quad (\text{or} \le)", 38),
             (r"\text{e.g.}", r":", r"M_t = \prod_{i \le t} \frac{q(X_i)}{p_0(X_i)} \text{ for any alternative } q", 36)],
            [r"fair starting capital", r"you cannot owe", r"a fair game under $H_0$", r"Part 44's betting paths"],
            colors=[(2, WEALTHC), (3, SPRTC)])

    def inequality(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Jean Ville proved in 1939 that a nonnegative martingale starting at one rarely gets large, "
            "at any time at all: <bookmark mark='b'/> the probability that it ever reaches one over alpha is at most alpha. "
            "<bookmark mark='c'/> That is Markov's inequality, but for the whole path at once rather than one fixed time. "
            "<bookmark mark='d'/> So the test that rejects the null the first time the martingale reaches twenty has "
            "type-one error at most five percent, however long you watch, and however you decide to stop.",
            [(r"\text{Ville (1939)}", r":", r"P_{H_0}\Big(\sup_{t \ge 0} M_t \ge \tfrac1\alpha\Big) \le \alpha", 40),
             (r"\text{e.g.}", r":", r"P(\text{ever } \ge 20) \le 5\%", 40),
             (r"\text{compare}", r":", r"\text{Markov: \ } P(M_t \ge 1/\alpha) \le \alpha \text{ at one } t", 38),
             (r"\text{test}", r":", r"\text{reject when } M_t \text{ first reaches } 1/\alpha", 38)],
            [r"Ville's thesis", r"the anytime guarantee", r"Markov, \ for the whole path", r"look as often as you like"],
            colors=[(0, WEALTHC), (3, CSC)])

    def proof(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The proof is optional stopping. Let tau be the first time the martingale reaches one over "
            "alpha, and stop there, or at a large time T if it never does. <bookmark mark='b'/> A stopped martingale is still "
            "a martingale, so its expected value at the stop is still one. <bookmark mark='c'/> On the event that it crossed, "
            "it is at least one over alpha; elsewhere it is at least zero. So one is at least the probability of crossing "
            "over alpha. <bookmark mark='d'/> Let T grow, and the bound holds for the supremum over all time.",
            [(r"\tau", r"=", r"\inf\{t: M_t \ge 1/\alpha\} \wedge T", 38),
             (r"E[M_\tau]", r"=", r"1 \quad (\text{optional stopping})", 38),
             (r"1", r"\ge", r"\tfrac1\alpha\,P(\tau \le T,\ M_\tau \ge \tfrac1\alpha)", 38),
             (r"T \to \infty", r":", r"P(\sup_t M_t \ge 1/\alpha) \le \alpha \qquad \blacksquare", 38)],
            [r"a stopping time", r"Part 44's theorem", r"Markov's step", r"monotone limit"],
            colors=[(3, CSC)])

    def peek_chart(self):
        d = load("ville")
        ns = np.log10(d["ns"])
        A = axes([-0.1, 3.8], [0, 0.65], x_length=7.4, y_length=4.4, xlabel=r"looks: \ after every observation, \ up to $n$ (log scale)",
                 ylabel=r"P(reject a true null)", xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 0.05, 0.25, 0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        pk = VGroup(polyline(ax, ns, d["curve"], FIXEDC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=FIXEDC) for a, b in zip(ns, d["curve"])])
        five = DashedLine(ax.c2p(-0.1, 0.05), ax.c2p(3.8, 0.05), color=CSC, stroke_width=2)
        vil = Dot(ax.c2p(3.0, d["ville"]), radius=0.1, color=WEALTHC)
        side = fit_rows(VGroup(
            label(r"red: \ the 5\% $z$-test, \ checked after every observation", font_size=22, color=FIXEDC),
            label(rf"by 100 looks {100 * d['curve'][6]:.0f}\%; \ by 5{{,}}000, \ {100 * d['curve'][-1]:.0f}\%", font_size=22, color=FIXEDC),
            label(rf"gold: \ Ville's test, \ $M_t \ge 20$, \ 1{{,}}000 looks: \ {100 * d['ville']:.1f}\%", font_size=22, color=WEALTHC),
            label(r"green: \ the promised 5\%", font_size=22, color=CSC),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The two tests, side by side, on twenty thousand null streams. In red, the ordinary five "
            f"percent z-test, checked after every observation. <bookmark mark='b'/> Its chance of a false rejection climbs: "
            f"{100 * d['curve'][6]:.0f} percent by a hundred looks, {100 * d['curve'][-1]:.0f} percent by five thousand. <bookmark "
            f"mark='c'/> In gold, the test that rejects when a likelihood-ratio martingale reaches twenty, watched for a "
            f"thousand observations: {100 * d['ville']:.1f} percent. <bookmark mark='d'/> Below the promised five percent, "
            f"as Ville said, however often we looked."
        ) as vo:
            self.play(FadeIn(A), Create(five), FadeIn(simulated_tag(r"simulated, \ 20{,}000 null streams")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pk), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(vil, scale=0.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(vil, color=WEALTHC))
        self.clear_scene()

    def paths(self):
        d = load("ville")
        t = np.log10(d["t"])
        A = axes([0, 3.0], [-4, 3.0], x_length=8.0, y_length=4.4, xlabel=r"observations (log scale)", ylabel=r"$\log_{10}$ wealth",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[-4, -2, 0, 1.3, 3], yfmt=lambda v: f"{v:g}", center=[-2.0, 0.2, 0])
        bp = BettingPaths(A.ax, t, d["null_paths"], ymin=-4, ymax=3)
        ba = BettingPaths(A.ax, t, d["alt_paths"], ymin=-4, ymax=3)
        side = fit_rows(VGroup(
            label(r"a gambler bets $\mu = 0.3$ against $\mu = 0$", font_size=22),
            label(r"blue: \ 40 null streams: \ wealth decays", font_size=22, color=SPRTC),
            label(rf"red: \ the {round(40 * d['null_cross'])} that touched 20: \ false alarms", font_size=22, color=FIXEDC),
            label(r"green: \ 12 streams at $\mu = 0.3$: \ wealth grows", font_size=22, color=CSC),
        ), 4.4, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same story as wealth. A gambler bets that the mean is point three rather than zero, "
            f"multiplying her capital by the likelihood ratio at each observation. <bookmark mark='b'/> On forty null streams "
            f"the wealth decays towards zero: betting against a true null loses. <bookmark mark='c'/> A few paths touch twenty "
            f"on the way, {round(40 * d['null_cross'])} of these forty; those are the false alarms, and Ville caps their "
            f"long-run share at five percent. <bookmark mark='d'/> When the mean really is point three, wealth grows "
            f"exponentially, and every path crosses twenty soon."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bp.threshold(0.05)), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bp.paths(SPRTC, 1.4, 0.5)), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(bp.crossers(0.05, FIXEDC)), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ba.paths(CSC, 2.0, 0.85)), FadeIn(side[3]), run_time=2.5)
        self.clear_scene()

    def sprt_again(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Chapter one's SPRT is a special case. Its likelihood ratio is a test martingale under the "
            "null. <bookmark mark='b'/> Rejecting when it reaches A, one minus beta over alpha, gives size at most one over A "
            "by Ville: the bound of chapter one, without any change of measure. <bookmark mark='c'/> What is new is that the "
            "upper boundary alone is enough: no lower boundary, no planned end. <bookmark mark='d'/> That is a test of power "
            "one: if the alternative is true it rejects eventually with probability one, and if the null is true it rejects "
            "with probability at most alpha, ever. Herbert Robbins and his colleagues studied such tests from the late 1960s.",
            [(r"\text{SPRT}", r":", r"\Lambda_t \text{ is a test martingale under } H_0", 38),
             (r"\text{Ville}", r":", r"P_0(\Lambda_t \text{ ever} \ge A) \le 1/A", 38),
             (r"\text{new}", r":", r"\text{no lower boundary, \ no planned end}", 38),
             (r"\text{power one}", r":", r"P_1(\text{reject eventually}) = 1", 38)],
            [r"chapter 1", r"the bound, \ in one line", r"open-ended", r"Robbins and colleagues"],
            colors=[(1, WEALTHC), (3, CSC)])

    def stopping(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What exactly is protected? Any stopping rule at all: stop when the result looks good, when "
            "the budget runs out, when a manager asks. <bookmark mark='b'/> At any stopping time, the stopped martingale is "
            "an e-value: its expectation under the null is at most one. <bookmark mark='c'/> So one over it is a valid p-value "
            "at that time, and continuing to collect data cannot hurt. <bookmark mark='d'/> What is not allowed is to change "
            "the bet after seeing the next observation: the bets must be predictable, chosen before the data they are "
            "applied to.",
            [(r"\text{any stopping rule}", r":", r"\text{good news, \ budgets, \ managers}", 38),
             (r"E_{H_0}[M_\tau]", r"\le", r"1 \text{ for every stopping time } \tau", 38),
             (r"\Rightarrow", r"\;", r"1/M_\tau \text{ is a valid } p\text{-value}", 38),
             (r"\text{but}", r":", r"\text{bets fixed before each observation is seen}", 38)],
            [r"the stopping rule is free", r"optional stopping", r"Markov", r"predictability"],
            colors=[(1, WEALTHC), (2, CSC), (3, FIXEDC)])

    def anytime_p(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The running minimum of one over M is an anytime-valid p-value: <bookmark mark='b'/> the "
            "probability, under the null, that it ever falls below alpha is at most alpha. <bookmark mark='c'/> Compare "
            "Part ten's p-value, valid only at the one sample size planned in advance. <bookmark mark='d'/> The price is "
            "power: an anytime-valid test is a little less powerful at any fixed time than the best fixed-sample test there, "
            "the price of insurance against every stopping rule.",
            [(r"p_t", r"=", r"\min_{s \le t} 1/M_s", 40),
             (r"P_{H_0}(\exists t: p_t \le \alpha)", r"\le", r"\alpha", 40),
             (r"\text{Part 10}", r":", r"\text{valid at one planned } n", 38),
             (r"\text{price}", r":", r"\text{less power at any fixed } n", 38)],
            [r"anytime-valid", r"Ville, \ restated", r"the fixed-$n$ $p$", r"insurance"],
            colors=[(1, CSC), (3, FIXEDC)])
