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
        self.lad_voiceover(
            "<bookmark mark='a'/> A confidence interval covers the parameter with probability one minus alpha at one sample "
            "size. A confidence sequence is a sequence of intervals, one for each time, that cover it at all times "
            "simultaneously, with probability one minus alpha. <bookmark mark='b'/> So the interval at any stopping time is "
            "a valid confidence interval, however the stopping time was chosen. <bookmark mark='c'/> Herbert Robbins and "
            "Donald Darling introduced them in 1967, and Robbins built them from mixtures in 1970. <bookmark mark='d'/> Every "
            "confidence sequence comes from inverting a family of test martingales, one for each candidate value.",
            [(r"\text{CI}", r":", r"P(\theta \in C_n) \ge 1 - \alpha \text{ at one } n", 38),
             (r"\text{CS}", r":", r"P(\theta \in C_t \text{ for all } t \ge 1) \ge 1 - \alpha", 38),
             (r"\text{history}", r":", r"\text{Darling \& Robbins (1967); \ Robbins (1970)}", 38),
             (r"\text{construction}", r":", r"C_t = \{\theta: M_t(\theta) < 1/\alpha\}", 38)],
            [r"fixed $n$", r"uniform in time", r"half a century early", r"invert Ville"],
            colors=[(1, CSC), (3, WEALTHC)])

    def mixture(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Robbins's normal mixture, for standard normal data with mean mu. For each bet lambda, e to "
            "the lambda times the centred sum, minus lambda squared t over two, is a test martingale. <bookmark mark='b'/> "
            "Average it over lambda drawn from a normal with variance tau squared: still a martingale, with a closed form. "
            "<bookmark mark='c'/> Ville says it stays below one over alpha forever with probability one minus alpha. "
            "<bookmark mark='d'/> Solving for mu gives the sequence: the running mean, plus or minus a width that shrinks "
            "like root of log t over t.",
            [(r"\text{for each } \lambda", r":", r"\exp\{\lambda S_t(\mu) - \lambda^2 t/2\}", 38),
             (r"\text{mix } \lambda \sim N(0, \tau^2)", r":", r"M_t = \frac{1}{\sqrt{1 + t\tau^2}}\exp\Big\{\frac{\tau^2 S_t^2}{2(1 + t\tau^2)}\Big\}", 36),
             (r"\text{Ville}", r":", r"M_t < 1/\alpha \text{ for all } t, \ \text{w.p.} \ge 1 - \alpha", 38),
             (r"\Rightarrow", r"\;", r"|\bar X_t - \mu| \le \frac{\sqrt{(1 + t\tau^2)\{\log(1 + t\tau^2) + 2\log(1/\alpha)\}}}{t\,\tau}", 34)],
            [r"$S_t(\mu) = \sum (X_i - \mu)$", r"a mixture of martingales", r"one inequality", r"width $\asymp \sqrt{\log t / t}$"],
            colors=[(1, WEALTHC), (3, CSC)])

    def lil(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> How narrow can a confidence sequence be? The law of the iterated logarithm sets the limit: "
            "a random walk reaches root of two t log log t infinitely often. <bookmark mark='b'/> So no sequence can shrink "
            "faster than root of log log t over t. The mixture's root log t is a little wider. <bookmark mark='c'/> Steven "
            "Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon stitched together boundaries over geometric epochs to "
            "reach the iterated-logarithm rate with explicit constants: <bookmark mark='d'/> for sub-Gaussian increments, one "
            "point seven times root of t times log log two t plus point seven two log of five point two over alpha.",
            [(r"\text{LIL}", r":", r"\limsup S_t/\sqrt{2t\log\log t} = 1", 38),
             (r"\Rightarrow", r"\;", r"\text{no CS narrower than } \sqrt{\log\log t / t}", 38),
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
            f"betting sequence of the next ladder. Both contain the truth throughout. <bookmark mark='e'/> The price: at five "
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
        self.lad_voiceover(
            "<bookmark mark='a'/> The betting sequence, from Ian Waudby-Smith and Ramdas, for any data bounded between zero "
            "and one. For each candidate mean m, a gambler bets on the next observation exceeding m, multiplying wealth by "
            "one plus lambda times X minus m. <bookmark mark='b'/> If m is the true mean, that is a fair bet, and wealth is a "
            "test martingale. <bookmark mark='c'/> The bet lambda is chosen from past data, aggressively when the past "
            "variance is small. <bookmark mark='d'/> The confidence sequence holds every m whose gamblers, betting both up "
            "and down, have not yet reached one over alpha. It adapts to the variance, as Part fifty-one's empirical "
            "Bernstein bounds do, without assuming anything but boundedness.",
            [(r"K_t(m)", r"=", r"\prod_{i \le t}\{1 + \lambda_i(X_i - m)\}", 38),
             (r"m = \mu", r":", r"E[1 + \lambda_i(X_i - \mu) \mid \mathcal F_{i-1}] = 1", 38),
             (r"\lambda_i", r":", r"\text{predictable, \ large when the variance is small}", 38),
             (r"C_t", r"=", r"\{m: \tfrac12 K_t^+(m) + \tfrac12 K_t^-(m) < 1/\alpha\}", 38)],
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
            f"promised, but at every time throughout only {100 * C['clt']['uniform']:.0f} percent. <bookmark mark='c'/> The "
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
        self.lad_voiceover(
            f"<bookmark mark='a'/> The cost, in width, at five thousand visitors, in percentage points either side. The fixed "
            f"CLT interval: {w('clt_lo', 'clt_hi'):.1f}. <bookmark mark='b'/> The betting sequence: {w('bet_lo', 'bet_hi'):.1f}, "
            f"about {w('bet_lo', 'bet_hi') / w('clt_lo', 'clt_hi'):.1f} times wider. <bookmark mark='c'/> Robbins's mixture: "
            f"{w('mix_lo', 'mix_hi'):.1f}; the stitched boundary: {w('stitch_lo', 'stitch_hi'):.1f}. <bookmark mark='d'/> And a "
            f"union bound over Hoeffding intervals, the naive way to make them hold at all times: {w('union_lo', 'union_hi'):.1f}. "
            f"Betting wins because it learns the variance; the price of watching continuously is a factor of about two in "
            f"width, not a factor that grows without limit.",
            [(r"\text{CLT, \ fixed } n", r":", rf"\pm {w('clt_lo', 'clt_hi'):.1f}", 40),
             (r"\text{betting CS}", r":", rf"\pm {w('bet_lo', 'bet_hi'):.1f}", 40),
             (r"\text{mixture, \ stitched}", r":", rf"\pm {w('mix_lo', 'mix_hi'):.1f}, \ \ \pm {w('stitch_lo', 'stitch_hi'):.1f}", 40),
             (r"\text{union of Hoeffdings}", r":", rf"\pm {w('union_lo', 'union_hi'):.1f}", 40)],
            [r"valid at one $t$ only", r"valid always", r"for $\sigma \le 1/2$", r"valid, \ wasteful"],
            colors=[(0, FIXEDC), (1, CSC)])

    def duality(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What to take away. <bookmark mark='b'/> A confidence sequence is a family of test "
            "martingales, inverted: test every candidate value, keep those not yet rejected. <bookmark mark='c'/> It may be "
            "watched continuously, stopped at any time, and extended with more data, keeping its coverage. <bookmark "
            "mark='d'/> Its width can approach the law of the iterated logarithm's limit, and adapts to the variance when "
            "built by betting. <bookmark mark='e'/> And online experimentation platforms have adopted always-valid inference, "
            "as Ramesh Johari and colleagues argued they should, because their users look every day.",
            [(r"what to take away:", GREY_A),
             (r"a CS = test martingales, \ one per candidate, \ inverted", WEALTHC),
             (r"watch continuously, \ stop at any time, \ extend with more data", CSC),
             (r"width near the LIL limit; \ betting adapts to the variance", CSC),
             (r"A/B platforms adopted always-valid inference \ (Johari et al.): \ users look daily", SPRTC)])
