from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Betting(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. Testing by betting: e-values, how to calibrate them, how to merge them, and how "
                       "to bet well.", 4, r"Testing by betting", r"Evidence as wealth", lit=(2021,))
        self.shafer()
        self.evalue()
        self.table()
        self.merge()
        self.merge_numbers()
        self.growth_chart()
        self.kelly()
        self.compare()

    def shafer(self):
        heading = label('Testing through conditionally fair bets', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Glenn Shafer proposed in 2021 that a test should be read as a bet. To test a "
            'hypothesis, offer a bet that costs one unit and has expected payoff at most one if the hypothesis is '
            "true. <bookmark mark='b'/> Its payoff, once the data arrive, measures the evidence: a payoff of twenty "
            "means the bet multiplied your money twenty-fold. <bookmark mark='c'/> A series of such bets, each "
            'staking the winnings of the last, is a nonnegative test supermartingale when each factor has '
            "conditional expectation at most one. <bookmark mark='d'/> The language changes what a result means: "
            'not a rare event under the null, but money won by betting against it.'
        ),
            [(r"\text{a bet}", r":", r"\text{costs } 1; \ E_{H_0}[\text{payoff}] \le 1", 38),
             (r"\text{evidence}", r"=", r"\text{the payoff: \ 20 means twentyfold}", 38),
             (r"\text{bets in series}", r":", r"\text{conditionally fair factors: \ a test supermartingale}", 38),
             (r"\text{reading}", r":", r"\text{money won against } H_0, \ \text{not a tail area}", 38)],
            [r"Shafer, \ \emph{JRSS A} (2021)", r"an e-value", r"chapter 3", r"a change of language"],
            colors=[(1, WEALTHC)])

    def evalue(self):
        heading = label('The e-value and calibrator definitions', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The payoff is an e-value: a nonnegative random variable whose expectation under "
            "the null is at most one. <bookmark mark='b'/> By Markov's inequality, the chance that it reaches one "
            "over alpha is at most alpha, so one over e is a valid p-value. <bookmark mark='c'/> The converse needs "
            'a calibrator: a decreasing function f with integral one over the unit interval turns any p-value into '
            "an e-value. <bookmark mark='d'/> Vladimir Vovk and Ruodu Wang's family, kappa p to the kappa minus "
            'one, is the standard choice.'
        ),
            [(r"E", r"\ge", r"0, \quad E_{H_0}[E] \le 1", 40),
             (r"e \to p", r":", r"p = \min(1, 1/E)", 40),
             (r"p \to e", r":", r"E = f(p), \ f \text{ decreasing}, \ \textstyle\int_0^1 f = 1", 38),
             (r"\text{Vovk--Wang}", r":", r"f_\kappa(p) = \kappa\,p^{\kappa - 1}, \ \kappa \in (0, 1)", 38)],
            [r"the definition", r"Markov", r"a calibrator", r"Vovk \& Wang (2021)"],
            colors=[(0, WEALTHC), (3, WEALTHC)])

    def table(self):
        d = load("evalues")
        hdr = [r"$p$-value", r"$e$, \ $\kappa = 1/2$", r"$e$, \ $\kappa = 1/10$", r"$1/p$ \ (not an e-value)"]
        body = [[f"{r['p']:g}", f"{r['e_half']:.2f}", f"{r['e_tenth']:.2f}", f"{1 / r['p']:.0f}"] for r in d["rows"]]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.9, row_buff=0.25, colors=[GREY_B] + [WHITE] * len(body)).move_to([0, 0.5, 0])
        foot = fit_rows(VGroup(
            label(r"calibrated e-values grow far more slowly than $1/p$: \ an e-value is a stricter currency", font_size=26, color=WEALTHC),
            label(r"with $\kappa=1/2$: \ $p=0.05$ maps to 2.24; \ the choice of calibrator matters", font_size=26, color=FIXEDC),
        ), 12.4, 0.25, [0, -2.6, 0])
        r05 = d["rows"][1]
        r001 = d["rows"][-1]
        with self.voiceover(
            f"<bookmark mark='a'/> What p-values are worth as e-values. <bookmark mark='b'/> With kappa a half, a p-value of five percent becomes an e-value of {say(r05['e_half'], 2)}; one in a thousand becomes {say(r001['e_half'], 1)}. With kappa a tenth, small p-values gain more and large ones less. <bookmark mark='c'/> One over p is not an universally valid e-value: its expectation is infinite for a uniform null p-value. Calibrated e-values grow much more slowly, a stricter currency. <bookmark mark='d'/> For the chosen half-power calibrator, five percent maps to about two. Another prechosen calibrator gives a different payoff; this is not a universal evidence value or posterior odds."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(exact_tag(r"exact arithmetic")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def merge(self):
        heading = label('Averages and conditionally fair products', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> E-values combine easily. The average of e-values is an e-value, whatever their "
            "dependence, because expectation is linear. <bookmark mark='b'/> The product of independent e-values is "
            'an e-value, and so is the product of sequential ones, each valid given the past: that is how a test '
            "martingale is built. <bookmark mark='c'/> P-values combine with difficulty: Fisher's method needs "
            'independence, and under arbitrary dependence valid rules, such as Bonferroni or twice the average '
            "p-value, pay a penalty. <bookmark mark='d'/> So e-values are the natural currency for evidence that "
            'accumulates across studies, sites or time, as in meta-analysis done as the studies arrive.'
        ),
            [(r"\text{average}", r":", r"\tfrac1K\textstyle\sum_k E_k \text{ is an e-value, \ any dependence}", 38),
             (r"\text{product}", r":", r"\textstyle\prod_k E_k \text{ is one, \ if independent or sequential}", 38),
             (r"p\text{-values}", r":", r"\text{Fisher needs independence; \ otherwise a penalty}", 38),
             (r"\text{so}", r":", r"\text{e-values: \ the currency for accumulating evidence}", 38)],
            [r"linearity", r"chapter 3's martingale", r"Vovk \& Wang (2020, 2021)", r"live meta-analysis"],
            colors=[(0, CSC), (1, CSC), (2, FIXEDC)])

    def merge_numbers(self):
        d = load("evalues")
        heading = label('Five independent studies', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> An illustration. Five independent studies of twenty observations each, a true effect of "
            f"point four standard deviations, and each study's e-value the likelihood ratio for an effect of a half. <bookmark "
            f"mark='b'/> A single study reaches twenty {100 * d['single_ge20']:.0f} percent of the time. <bookmark mark='c'/> "
            f"The average of the five, valid under any dependence, reaches twenty {100 * d['mean_ge20']:.0f} percent of the "
            f"time. <bookmark mark='d'/> The product, valid because they are independent, reaches it "
            f"{100 * d['prod_ge20']:.0f} percent of the time: evidence multiplies.",
            [(r"\text{five studies}", r":", r"n = 20 \text{ each, \ } \mu = 0.4, \ \text{bet on } 0.5", 38),
             (r"\text{one}", r":", rf"P(E \ge 20) = {100 * d['single_ge20']:.0f}\%", 38),
             (r"\text{average}", r":", rf"{100 * d['mean_ge20']:.0f}\%", 38),
             (r"\text{product}", r":", rf"{100 * d['prod_ge20']:.0f}\%", 38)],
            [r"simulated", r"a single bet", r"robust to dependence", r"evidence multiplies"],
            colors=[(3, CSC)])

    def growth_chart(self):
        d = load("evalues")
        mus = np.asarray(d["mus"])
        A = axes([0, 1], [-0.35, 0.55], x_length=7.4, y_length=4.4, xlabel=r"true mean $\mu$ \ (data $N(\mu, 1)$)", ylabel=r"growth: \ $E \log$ wealth per observation",
                 xticks=[0, 0.5, 1], yticks=[-0.25, 0, 0.25, 0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0.2": SPRTC, "0.5": WEALTHC, "1.0": FIXEDC}
        lines = [polyline(ax, mus, d["growth"][k], cols[k], 4) for k in ("0.2", "0.5", "1.0")]
        best = polyline(ax, mus, mus ** 2 / 2, CSC, 3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1, 0), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"bet $b$: \ multiply wealth by $e^{bX - b^2/2}$", font_size=22),
            label(r"growth $b\mu - b^2/2$: \ blue $b = 0.2$, \ gold 0.5, \ red 1", font_size=22, color=WEALTHC),
            label(r"green: \ the best growth, \ $\mu^2/2$, \ at $b = \mu$", font_size=22, color=CSC),
            label(r"overbetting is worse than underbetting: \ red goes negative", font_size=22, color=FIXEDC),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            (
            "<bookmark mark='a'/> How should one bet? Betting b on normal data multiplies wealth by e to the b X "
            "minus b squared over two. <bookmark mark='b'/> Its growth rate, the expected log of wealth per "
            'observation, is b mu minus b squared over two: three bets, three straight lines in mu. <bookmark '
            "mark='c'/> The best growth, mu squared over two, comes from betting exactly the true mean. <bookmark "
            "mark='d'/> And overbetting is worse than underbetting: bet one when the mean is a quarter, and wealth "
            'shrinks even though the null is false.'
        )
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(exact_tag(r"exact arithmetic")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(best), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(lines[2], color=FIXEDC))
        self.clear_scene()

    def kelly(self):
        heading = label('Expected log growth and betting error', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Validity asks whether the bet is fair under the null. Efficiency asks how rapidly "
            "wealth grows under an alternative. Kelly's criterion maximizes expected log wealth. <bookmark "
            "mark='b'/> For a simple null and a specified alternative, the likelihood ratio is log optimal. A "
            'predictable fitted alternative also gives fair likelihood-ratio factors when each candidate is a '
            "proper density. <bookmark mark='c'/> In the unit-variance normal example, betting on mean b when the "
            'truth is mu gives growth b mu minus b squared over two. It is maximized at b equal to mu. <bookmark '
            "mark='d'/> The growth loss is half the squared betting error, symmetric for equal overestimates and "
            'underestimates. A very oversized bet can lose money even under the alternative. Composite nulls '
            'require fairness against every null member.'
        ),
            [(r"\text{Kelly (1956)}", r":", r"\max E\log(\text{wealth})", 38),
             (r"\text{simple vs simple}", r":", r"\text{bet the likelihood ratio; \ growth } \mathrm{KL}(q \,\|\, p_0)", 36),
             (r"\text{unknown } q", r":", r"\text{mix over it, \ or plug in } \hat q_{t-1}", 38),
             (r"\text{validity}", r":", r"\text{proper predictable density vs a simple conditional null}", 38)],
            [r"log-optimal betting", r"chapter 1's drift", r"mixture or plug-in", r"predictable bets"],
            colors=[(1, WEALTHC), (3, CSC)])

    def compare(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> A p-value describes a tail probability under a null model; an e-value is a "
            'nonnegative payoff with null expectation at most one. Both can support valid tests. <bookmark '
            "mark='b'/> Fixed-sample e-values are convenient to average, while independent or conditionally fair "
            "factors can be multiplied. <bookmark mark='c'/> A collection of e-values valid at separate fixed times "
            'is not automatically an e-process. Validity at stopping times needs an additional sequential '
            "construction. <bookmark mark='d'/> Likewise, anytime-valid p-values are possible. <bookmark mark='e'/> "
            'The practical distinction is the guarantee of the particular construction, rather than the letter used '
            'to report evidence.'
        ),
            [('Combining $p$-values and e-values in sequential analysis', GREY_A),
             (r"both $p$-values and e-values can be fixed-sample or anytime-valid", CSC),
             (r"combine with difficulty \ $|$ \ average under any dependence, \ multiply in sequence", CSC),
             (r"surprise under $H_0$ \ $|$ \ money won, \ optimized by Kelly's criterion", WEALTHC),
             (r"sequential validity is an additional guarantee, \ not automatic", FIXEDC)], head_size=36)
