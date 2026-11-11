from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MID_C, OFI_C, PART, comma, load)


class Events(VoiceoverScene):
    def construct(self):
        me = load("memory")
        self.card()
        self.hawkes(me)
        self.fit(me)
        self.critical()
        self.cluster()
        self.signs(me)
        self.split()
        self.signature_(me)
        self.pairs()
        self.question()

    def card(self):
        c = chapter_card(3, r"Events that cause events", r"Why do orders arrive in bursts, and why do their signs repeat?",
                         part=PART)
        with self.voiceover("Chapter three. Orders do not arrive like raindrops. They come in bursts, and buy orders "
                            "follow buy orders for minutes on end. Two facts, measured, and what they imply."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def hawkes(self, me):
        rows = [cmath(r"\lambda(t)", r"=", r"\mu + \textstyle\sum_{t_i < t} \alpha e^{-\beta (t - t_i)}", font_size=38,
                      colors={r"\lambda(t)": OFI_C}),
                cmath(r"n", r"=", r"\alpha/\beta\ \ \text{(the branching ratio)}", font_size=36),
                cmath(r"\text{mean rate}", r"=", r"\frac{\mu}{1 - n}", font_size=36)]
        whys = [why(r"Part 5's Hawkes process: every event raises the rate of further events, which then decays"),
                why(r"the expected number of events each event causes directly"),
                why('for a stationary positive linear cluster model, $n<1$ is the latent offspring share; not an identified causal reaction fraction')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A positive linear exponential Hawkes model. <bookmark mark='a'/> Its conditional intensity is a positive background rate plus decaying contributions from past events. <bookmark mark='b'/> With nonnegative alpha and positive beta, the kernel integral n is alpha over beta. In the model's Poisson-cluster representation it is the expected number of direct offspring. <bookmark mark='c'/> For a stationary version with n below one, the mean rate is mu over one minus n and the latent offspring share is n. A fitted branching ratio is not an observed causal fraction of traders reacting to one another."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def fit(self, me):
        h = me["hawkes"]
        dll = h["loglik"] - h["loglik_poisson"]
        rows = [cmath(r"\hat n", r"=", rf"{h['branching']:.2f}", font_size=40, colors={r"\hat n": OFI_C}),
                cmath(r"\Delta\log L", r"=", rf"{comma(dll)}\ \text{{over Poisson}}", font_size=34),
                cmath(r"\text{KS of rescaled gaps}", r"=", rf"{me['ks']:.3f}\ \ (\text{{Poisson: }}{me['ks_poisson']:.3f})",
                      font_size=30, colors={r"\text{KS of rescaled gaps}": BAD})]
        whys = [why(f"one hour of BTCUSDT trades, {comma(me['n_events'])} arrivals, fitted by maximum likelihood with Part 5's code: branching is a fitted cluster-model parameter, not observed causation"),
                why('in-sample likelihood comparison; Hawkes has more parameters'),
                why('descriptive KS statistic with fitted parameters and dependent gaps; no calibrated goodness-of-fit p-value')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""The fitted hour contains {h['n']:,} distinct rounded-millisecond arrival times after deduplication. <bookmark mark='a'/> Its estimated branching ratio is {h['branching']:.2f}, a model parameter rather than an identified reaction fraction. <bookmark mark='b'/> The in-sample log likelihood exceeds the Poisson fit by {dll:,.0f}; the Hawkes model also has more parameters. <bookmark mark='c'/> The displayed rescaled-gap KS statistic is descriptive. The same events estimate the parameters and test the fit, and the gaps may remain dependent. No calibrated goodness-of-fit p-value or causal attribution follows from this statistic alone."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def critical(self):
        cards = VGroup(
            desk_question(r"many time scales", r"with a power-law kernel spanning microseconds to hours, Hardiman, Bercot "
                          r"and Bouchaud (2013) estimated branching ratios close to one on index futures", width=12.4,
                          font_size=19),
            desk_question(r"near-criticality", 'within a stationary positive cluster model, high branching means a large latent offspring share; not identified trader causation', width=12.4, font_size=19),
            desk_question(r"and rough volatility", 'Part 14: nearly unstable Hawkes processes with power-law kernels can yield rough-volatility limits under specified heavy-tail, near-instability and price scaling', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three distinct claims. <bookmark mark='a'/> Hardiman, Bercot and Bouchaud estimated high branching ratios under long-memory Hawkes specifications on index futures. The estimate depends on kernel, sample window and background specification. <bookmark mark='b'/> Near one, the stationary positive cluster model has large average families and strong amplification. This interpretation is conditional on the model. <bookmark mark='c'/> Certain nearly unstable heavy-tailed Hawkes models, under specified time, intensity and price scaling, have rough-volatility limits. A single exponential-kernel fit to this hour does not establish that limit or explain all daily volatility."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cluster(self):
        rows = [cmath(r"\lambda(t)", r"=", r"\mu + \textstyle\sum_{t_i < t} \alpha e^{-\beta (t - t_i)}", font_size=36),
                cmath(r"n", r"=", r"\alpha / \beta", font_size=40, colors={r"n": HURDLE}),
                cmath(r"\mathbb E[\text{cluster size}]", r"=", r"1 + n + n^2 + \cdots = \frac{1}{1 - n}", font_size=36),
                cmath(r"\bar\lambda", r"=", r"\frac{\mu}{1 - n}", font_size=40, colors={r"\bar\lambda": GOOD})]
        whys = [why(r"Hawkes (1971): every event raises the rate of future events, and the boost decays"),
                why(r"the branching ratio: the expected number of direct offspring of one event, the area under the "
                    r"kernel"),
                why(r"Hawkes and Oakes (1974): each background event starts a family tree of children, grandchildren "
                    r"and so on; the family is finite on average only if $n < 1$"),
                why(r"so the mean rate is the background rate times the mean family size; as $n \to 1$ nearly all events "
                    r"are caused by other events")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The cluster calculation within the stipulated positive linear model. <bookmark mark='a'/> Background immigrants arrive at rate mu. <bookmark mark='b'/> Each event has expected n direct children, the integral of the kernel. <bookmark mark='c'/> When n is below one, the expected family size including the immigrant is the geometric sum, one over one minus n. At n equal to one the mean diverges; above one a finite stationary mean is unavailable. <bookmark mark='d'/> Multiplying family size by immigration rate gives mu over one minus n. The latent genealogy is a representation of the model, not a recovered family tree for the observed trades."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def signs(self, me):
        lags = np.log10(np.asarray(me["lags"], float))
        acf = np.asarray(me["acf"], float)
        ok = acf > 0
        g = axes([0, 3.5], [-2.6, 0], x_length=7.0, y_length=4.4, xlabel=r"lag, trades ($\log_{10}$)",
                 ylabel=r"$\log_{10}$ autocorrelation of trade signs", xticks=[0, 1, 2, 3], yticks=[-2, -1, 0],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=OFI_C) for a, b in zip(lags[ok], acf[ok])])
        gm = me["gamma"]
        fit_ok = ok & (lags >= 1)
        b0 = float(np.mean(np.log10(acf[fit_ok]) + gm * lags[fit_ok]))
        line = Line(ax.c2p(1, b0 - gm), ax.c2p(3.4, b0 - 3.4 * gm), color=HURDLE, stroke_width=2)
        st = label(rf"slope $-\gamma = -{gm:.2f}$", font_size=18, color=HURDLE).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        with self.voiceover(
            f"""A finite-sample sign-memory diagnostic. <bookmark mark='a'/> Plot buy-sell sign autocorrelation against event lag on logarithmic axes. <bookmark mark='b'/> A line fitted to the positive correlations at selected lags has exponent about {gm:.2f}. No interval is computed, and choosing positive values affects the fit. A true asymptotic power law with exponent between zero and one has nonsummable correlations; this finite window alone does not prove asymptotic long memory or identify order splitting."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def split(self):
        rows = [cmath(r"\text{metaorder}", r":", r"\text{a large order cut into many small ones}", font_size=32,
                      colors={r"\text{metaorder}": OFI_C}),
                cmath(r"\Pr(\text{size} > L)", r"\sim", r"L^{-\alpha}\ \Rightarrow\ C(\ell) \sim \ell^{-(\alpha - 1)}",
                      font_size=32),
                cmath(r"\text{efficiency}", r":", '\\text{persistent signs, weak return predictability}', font_size=32,
                      colors={r"\text{efficiency}": HURDLE})]
        whys = [why(r"institutions slice their orders (Part 37), so the signs of child orders repeat"),
                why(r"Lillo, Mike and Farmer (2005): if metaorder sizes have a power-law tail, the sign autocorrelation "
                    r"decays as a power law, with an exponent set by the tail"),
                why('adaptive impact and liquidity can reconcile persistent signs with weak return predictability in specified models')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "One mechanism for persistent signs. <bookmark mark='a'/> A large parent order can be split into many same-side child orders. <bookmark mark='b'/> In the particular splitting model, a parent-size tail exponent between one and two leads to a sign-correlation exponent alpha minus one. Other scheduling, participation and dependence assumptions can change that mapping. <bookmark mark='c'/> Persistent order signs can coexist with weak return predictability if impact and liquidity adapt. This is a model reconciliation, not evidence that prices are exactly unpredictable or that splitting uniquely caused the observed autocorrelation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def signature_(self, me):
        steps = np.asarray(me["steps"], float)
        sig = np.asarray(me["signature"], float)
        x = np.log10(steps * 0.1)
        g = axes([-1.2, 2.0], [0.3, 0.46], x_length=7.0, y_length=4.4, xlabel=r"sampling interval, seconds ($\log_{10}$)",
                 ylabel='mean squared mid increment per 100 ms, \\$$^2$', xticks=[-1, 0, 1], yticks=[0.3, 0.38, 0.46],
                 xfmt=lambda v: f"{10 ** v:g}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, x, sig, MID_C, stroke_width=3)
        d1 = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=MID_C) for a, b in zip(x, sig)])
        rise = 100 * (sig.max() / sig[0] - 1)
        with self.voiceover(
            f"""A signature diagnostic in explicit units. <bookmark mark='a'/> The code averages squared mid increments at each sampling step and divides by the number of hundred-millisecond grid steps, not by seconds. The vertical unit is squared dollars per hundred milliseconds; multiply by ten for squared dollars per second. It is a second moment rather than a demeaned variance. <bookmark mark='b'/> The largest sampled value is about {rise:.0f} percent above the shortest-step value. Such horizon dependence is consistent with serial dependence and aggregation effects, but it does not identify their cause. Transaction-price bid-ask bounce and quote-mid dynamics are different objects."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(d1))
        self.wait(0.4)
        self.clear_scene()

    def pairs(self):
        rows = [cmath(r"\text{one-tick spread}", r":", r"\text{the offer empties} \Rightarrow \text{mid} + \tfrac12\text{tick}",
                      font_size=30),
                cmath(r"\text{then}", r":", r"\text{a new bid closes the gap} \Rightarrow \text{mid} + \tfrac12\text{tick}",
                      font_size=30),
                cmath(r"\text{mid moves}", '\\quad\\text{may form}\\quad', r"\text{same-direction pairs}", font_size=32,
                      colors={r"\text{same-direction pairs}": HURDLE})]
        whys = [why(r"when the best offer is exhausted, the spread opens to two ticks and the mid rises half a tick"),
                why('in this illustrative sequence, a new bid inside the widened spread raises the mid another half tick'),
                why('this mechanism can generate same-direction mid moves; the diagram does not identify its frequency or explain every signature-plot feature')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A possible quote-refill mechanism. <bookmark mark='a'/> Start with a one-tick spread. If only the best offer disappears and the next offer is one tick higher, the midpoint rises half a tick and the spread widens. <bookmark mark='b'/> If a new bid then joins inside that gap, the midpoint rises another half tick while the spread narrows. <bookmark mark='c'/> This stipulated two-step sequence creates same-direction midpoint moves. Other quote sequences need not do so. The illustration neither estimates its frequency nor proves that it caused the measured signature curve."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        head = label('Stationarity before interpreting branching', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('\\mu=2\\ \\mathrm{s}^{-1},\\quad n=0.68\\ \\text{or}\\ 0.95,\\qquad \\bar\\lambda=\\frac\\mu{1-n}', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('Positive stationary linear Hawkes cluster model. The expected family includes its immigrant.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Compute mean family sizes and event rates. What changes at n=1?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('Within a stationary positive linear Hawkes model, let immigration be two events per second. Compute expected family size including the immigrant and mean event rate when branching is point six eight and point nine five. State what happens to the finite stationary mean at one. Explain why the model offspring fraction is not an observed causal trader-reaction fraction.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
