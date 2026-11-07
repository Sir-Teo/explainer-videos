from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class ConfidenceSequences(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Confidence sequences: intervals that hold at every time at once, so you may "
                       "watch them shrink and stop when you like.", 6, r"Confidence sequences", r"Intervals valid at every time",
                       lit=(1970,))
        self.definition()
        self.mixture()
        self.lil()
        self.funnel()
        self.betting_idea()
        self.coverage_table()
        self.board()
        self.widths()
        self.duality()

    def definition(self):
        heading = label('The guarantee and its assumptions', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A confidence interval covers the parameter with probability one minus alpha at "
            'one sample size. A confidence sequence is a sequence of intervals, one for each time, that cover it at '
            "all times simultaneously, with probability one minus alpha. <bookmark mark='b'/> So the interval at "
            'any stopping time is a valid confidence interval, however the stopping time was chosen. <bookmark '
            "mark='c'/> Herbert Robbins and Donald Darling introduced them in 1967, and Robbins built them from "
            "mixtures in 1970. <bookmark mark='d'/> One useful construction inverts a family of anytime-valid "
            'tests, for example test martingales, one for each candidate value.'
        ),
            [(r"\text{CI}", r":", r"P(\theta \in C_n) \ge 1 - \alpha \text{ at one } n", 38),
             (r"\text{CS}", r":", r"P(\theta \in C_t \text{ for all } t \ge 1) \ge 1 - \alpha", 38),
             (r"\text{history}", r":", r"\text{Darling \& Robbins (1967); \ Robbins (1970)}", 38),
             (r"\text{construction}", r":", r"C_t = \{\theta: M_t(\theta) < 1/\alpha\}", 38)],
            [r"fixed $n$", r"uniform in time", r"half a century early", r"invert Ville"],
            colors=[(1, CSC), (3, WEALTHC)])

    def mixture(self):
        heading = label("Robbins's Gaussian mixture", font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Robbins's normal mixture, for standard normal data with mean mu. For each bet "
            'lambda, e to the lambda times the centred sum, minus lambda squared t over two, is a test martingale. '
            "<bookmark mark='b'/> Average it over lambda drawn from a normal with variance tau squared: still a "
            "martingale, with a closed form. <bookmark mark='c'/> Ville says it stays below one over alpha forever "
            "with probability one minus alpha. <bookmark mark='d'/> Solving for mu gives the sequence: the running "
            'mean, plus or minus a width that shrinks like root of log t over t.'
        ),
            [(r"\text{for each } \lambda", r":", r"\exp\{\lambda S_t(\mu) - \lambda^2 t/2\}", 38),
             (r"\text{mix } \lambda \sim N(0, \tau^2)", r":", r"M_t = \frac{1}{\sqrt{1 + t\tau^2}}\exp\Big\{\frac{\tau^2 S_t^2}{2(1 + t\tau^2)}\Big\}", 36),
             (r"\text{Ville}", r":", r"M_t < 1/\alpha \text{ for all } t, \ \text{w.p.} \ge 1 - \alpha", 38),
             (r"\Rightarrow", r"\;", r"|\bar X_t - \mu| \le \frac{\sqrt{(1 + t\tau^2)\{\log(1 + t\tau^2) + 2\log(1/\alpha)\}}}{t\,\tau}", 34)],
            [r"$S_t(\mu) = \sum (X_i - \mu)$", r"a mixture of martingales", r"one inequality", r"width $\asymp \sqrt{\log t / t}$"],
            colors=[(1, WEALTHC), (3, CSC)])

    def lil(self):
        heading = label('Iterated-logarithm rates and their scope', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The law of the iterated logarithm describes the fluctuations of a nondegenerate "
            "IID centered sum after variance normalization. <bookmark mark='b'/> For ordinary intervals centered on "
            'the sample mean, this prevents an eventual half-width smaller than the iterated-logarithm scale. It is '
            "not a pointwise lower bound on every imaginable confidence sequence. <bookmark mark='c'/> Stitching "
            'boundaries over geometric epochs attains this rate with explicit constants. The fixed normal mixture '
            "instead has a root log t factor. <bookmark mark='d'/> The displayed one-sided stitched bound applies "
            'to conditionally one-sub-Gaussian centered increments. For bounded zero-to-one data, one-half is a '
            'valid sub-Gaussian scale.'
        ),
            [(r"\text{LIL}", r":", r"\limsup S_t/\sqrt{2t\log\log t} = 1", 38),
             (r"\Rightarrow", r"\;", r"\text{sample-mean centered widths need the LIL scale}", 38),
             (r"\text{stitching}", r":", r"\text{boundaries over epochs } [\eta^k, \eta^{k+1})", 38),
             (r"\text{one-sided}", r":", r"S_t \le 1.7\sqrt{t\,\{\log\log(2t) + 0.72\log(5.2/\alpha)\}}", 36)],
            [r"Part 44", r"the lower limit", r"peeling, \ made exact", r"Howard et al., \ \emph{Ann. Stat.} (2021)"],
            colors=[(1, FIXEDC), (3, CSC)])

    def funnel(self):
        d = load("cs")
        S = d["series"]
        t = np.asarray(S["t"])
        lt = np.log10(t)
        A = axes([0, math.log10(d["T"]) + 0.02], [0, 0.4], x_length=8.2, y_length=4.6, xlabel=r"visitors (log scale)", ylabel=r"conversion rate",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 0.12, 0.2, 0.4], center=[-2.0, 0.2, 0])
        F = ConfidenceFunnel(A.ax, t, S["xbar"])
        clt = F.band(S["clt_lo"], S["clt_hi"], FIXEDC, opacity=0.25)
        mix = F.band(S["mix_lo"], S["mix_hi"], SPRTC, opacity=0.12)
        bet = F.band(S["bet_lo"], S["bet_hi"], CSC, opacity=0.25)
        est = F.estimate(WHITE)
        tru = F.truth(d["p"], WEALTHC)
        miss = F.misses(S["clt_lo"], S["clt_hi"], d["p"], FIXEDC)
        fin = d["final"]
        side = fit_rows(VGroup(
            label(rf"one stream: \ true rate {100 * d['p']:.0f}\% \ (gold), \ running mean (white)", font_size=22),
            label(r"red: \ the 95\% CLT interval at each $t$", font_size=22, color=FIXEDC),
            label(rf"red dots: \ times it excluded the truth \ ({len(miss)} of {len(t)} shown)", font_size=22, color=FIXEDC),
            label(r"blue: \ Robbins's normal mixture; \ green: \ the betting CS", font_size=22, color=CSC),
            label(rf"at 5{{,}}000: \ CLT $\pm${100 * (fin['clt_hi'] - fin['clt_lo']) / 2:.1f}, \ betting $\pm${100 * (fin['bet_hi'] - fin['bet_lo']) / 2:.1f} points", font_size=22, color=GREY_A),
        ), 4.2, 0.36, [4.6, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The confidence funnel, this part's instrument, on one stream from the World's A/B "
            f"platform: visitors convert with probability twelve percent, and time runs on a log scale. <bookmark mark='b'/> "
            f"In red, the ordinary ninety-five percent interval recomputed at each visitor. <bookmark mark='c'/> The red dots "
            f"mark the times it excluded the truth: {len(miss)} of the {len(t)} times drawn. Anyone stopping at one of them "
            f"would have reported a wrong interval. <bookmark mark='d'/> In blue, Robbins's mixture sequence; in green, the "
            f"betting sequence of the next ladder. For these Bernoulli data the normal mixture uses the Hoeffding sub-Gaussian scale one-half, giving a supermartingale rather than an exact Gaussian martingale. Both bands contain the truth throughout on this stream. <bookmark mark='e'/> The price: at five "
            f"thousand visitors the betting sequence is plus or minus {100 * (fin['bet_hi'] - fin['bet_lo']) / 2:.1f} points, "
            f"against {100 * (fin['clt_hi'] - fin['clt_lo']) / 2:.1f} for the fixed interval."
        ) as vo:
            self.play(FadeIn(A), Create(tru), FadeIn(simulated_tag(r"the World's A/B platform")))
            vo.wait_until("a")
            self.play(Create(est), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(clt), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in miss], lag_ratio=0.05), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(mix), FadeIn(bet), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def betting_idea(self):
        heading = label('A continuum confidence set from bounded-mean bets', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Betting confidence sequences need bounded observations and a common conditional "
            "mean: the next observation's expectation given the past is mu. Marginal boundedness alone does not "
            "suffice. <bookmark mark='b'/> At the true candidate mean, one plus a predictable stake times the "
            'centered observation has conditional expectation one. Cap the stake to keep every factor nonnegative. '
            "<bookmark mark='c'/> Our predictable plug-in stakes use past variance, with separate upward and "
            'downward gamblers. This illustrative rule is not claimed to attain the optimal iterated-logarithm '
            "rate. <bookmark mark='d'/> We keep the running intersection of candidates whose hedged wealth has not "
            'crossed. Numerically we exclude whole grid cells only using a lower wealth bound, then return an outer '
            'interval. This preserves continuum coverage, including means between grid nodes and the endpoints.'
        ),
            [(r"K_t(m)", r"=", r"\prod_{i \le t}\{1 + \lambda_i(X_i - m)\}", 38),
             (r"m = \mu", r":", r"E[1 + \lambda_i(X_i - \mu) \mid \mathcal F_{i-1}] = 1", 38),
             (r"\lambda_i", r":", r"\text{predictable, \ large when the variance is small}", 38),
             (r"C_t", r"=", r"\{m: \max_{s\le t}(\tfrac12 K_s^+(m)+\tfrac12 K_s^-(m))<1/\alpha\}", 38)],
            [r"Waudby-Smith \& Ramdas (2024)", r"a fair bet", r"chosen from the past", r"hedged: \ up and down"],
            colors=[(0, WEALTHC), (3, CSC)])

    def coverage_table(self):
        d = load("cs")
        C = d["coverage"]
        hdr = [r"method", r"covers at every $t \in [20, 2{,}000]$", r"covers at $t = 2{,}000$"]
        names = [("clt", r"95\% CLT interval, \ each $t$"), ("hoeffding", r"95\% Hoeffding interval, \ each $t$"),
                 ("mixture", r"normal-mixture CS"), ("betting", r"betting CS")]
        body = [[nm, f"{100 * C[k]['uniform']:.1f}\\%", f"{100 * C[k]['final']:.1f}\\%"] for k, nm in names]
        cols = [GREY_B, FIXEDC, GREY_A, SPRTC, CSC]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.3, colors=cols).move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['reps']} streams at a 12\% rate, \ watched from visitor 20 to 2{{,}}000", font_size=24, color=GREY_A),
            label(r"Hoeffding's fixed interval survives here only because it ignores the variance: \ $p(1-p) = 0.11 \ll 1/4$", font_size=24, color=GREY_A),
        ), 12.4, 0.22, [0, -2.5, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Over {d['reps']} streams, watched from the twentieth visitor to the two-thousandth. "
            f"<bookmark mark='b'/> The CLT interval covers at the end {100 * C['clt']['final']:.0f} percent of the time, as "
            f"expected approximately at this fixed sample size, but throughout only {100 * C['clt']['uniform']:.0f} percent. <bookmark mark='c'/> The "
            f"two confidence sequences hold throughout: the mixture {100 * C['mixture']['uniform']:.0f} percent, the betting "
            f"sequence {100 * C['betting']['uniform']:.1f}. <bookmark mark='d'/> Hoeffding's fixed interval also survives here, "
            f"but only because it ignores the variance and is far too wide for a rate of twelve percent: lucky, not valid."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"the World's A/B platform")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(tab[2]), FadeIn(foot[1]))
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("checked every visit", "betting confidence"),
                   f"<bookmark mark='a'/> On the Board: the fixed interval, checked at every visit, covers throughout in "
                   f"{100 * br[0]['achieved']:.0f} percent of streams: broken. <bookmark mark='b'/> The betting confidence "
                   f"sequence covers throughout in {100 * br[1]['achieved']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def widths(self):
        d = load("cs")
        f = d["final"]
        w = lambda a, b: 100 * (f[b] - f[a]) / 2  # noqa: E731
        heading = label('Half-widths at this sample size', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> The cost, in width, at five thousand visitors, in percentage points either side. The fixed CLT interval: {w('clt_lo', 'clt_hi'):.1f}. <bookmark mark='b'/> The betting sequence: {w('bet_lo', 'bet_hi'):.1f}, about {w('bet_lo', 'bet_hi') / w('clt_lo', 'clt_hi'):.1f} times wider. <bookmark mark='c'/> Robbins's mixture: {w('mix_lo', 'mix_hi'):.1f}; the stitched boundary: {w('stitch_lo', 'stitch_hi'):.1f}. <bookmark mark='d'/> And a union bound over Hoeffding intervals, the naive way to make them hold at all times: {w('union_lo', 'union_hi'):.1f}. Here variance adaptation gives the narrowest displayed sequence. The factor of about two is specific to this sample size and path. Relative to a fixed-sample interval, even an iterated-logarithm width factor can grow slowly without bound.",
            [(r"\text{CLT, \ fixed } n", r":", rf"\pm {w('clt_lo', 'clt_hi'):.1f}", 40),
             (r"\text{betting CS}", r":", rf"\pm {w('bet_lo', 'bet_hi'):.1f}", 40),
             (r"\text{mixture, \ stitched}", r":", rf"\pm {w('mix_lo', 'mix_hi'):.1f}, \ \ \pm {w('stitch_lo', 'stitch_hi'):.1f}", 40),
             (r"\text{union of Hoeffdings}", r":", rf"\pm {w('union_lo', 'union_hi'):.1f}", 40)],
            [r"valid at one $t$ only", r"valid always", r"for $\sigma \le 1/2$", r"valid, \ wasteful"],
            colors=[(0, FIXEDC), (1, CSC)])

    def duality(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> What to take away. <bookmark mark='b'/> A confidence sequence can be built by "
            'inverting anytime-valid tests: test every candidate value, keep those not yet rejected. <bookmark '
            "mark='c'/> It may be watched continuously, stopped at any time, and extended with more data, keeping "
            "its coverage. <bookmark mark='d'/> Its width can approach the law of the iterated logarithm's limit, "
            "and adapts to the variance when built by betting. <bookmark mark='e'/> And online experimentation "
            'platforms have adopted always-valid inference, as Ramesh Johari and colleagues argued they should, '
            'because their users look every day.'
        ),
            [('Confidence sequences: guarantees and efficiency', GREY_A),
             (r"a CS construction: \ invert an anytime-valid test per candidate", WEALTHC),
             (r"watch continuously, \ stop at any time, \ extend with more data", CSC),
             (r"width near the LIL limit; \ betting adapts to the variance", CSC),
             (r"A/B platforms adopted always-valid inference \ (Johari et al.): \ users look daily", SPRTC)], head_size=36)
