from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, ask, illustration, load


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


class Monitor(VoiceoverScene):
    def construct(self):
        m = load("monitor")
        self.card()
        self.peeking()
        self.bet()
        self.example(m["examples"]["flagged"], BAD)
        self.example(m["examples"]["kept"], GOOD)
        self.zoo(m)
        self.question()

    def card(self):
        c = chapter_card(12, r"Monitoring live strategies with e-values", r"When has a strategy stopped working?",
                         lit=(2016,), part=PART)
        with self.voiceover("Chapter twelve. After the backtest comes the live record, and the question every fund "
                            "asks every month: has it stopped working?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def peeking(self):
        cards = VGroup(
            desk_question(r"the monthly $t$-test", r"look at a live strategy every month with a 5\% test, and over ten "
                          r"years you will raise a false alarm far more often than 5\% of the time: each look is another "
                          r"chance", width=12.2, font_size=20),
            desk_question(r"the fixed horizon", r"or decide to look only once, after five years, and accept five years of "
                          r"losses from a strategy that died in the first", width=12.2, font_size=20),
            desk_question(r"testing by betting (Part 4)", r"bet against the strategy's claim; your wealth is a "
                          r"nonnegative martingale if the claim is true, and Ville's inequality bounds the chance it ever "
                          r"reaches $1/\alpha$, however often you look", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two bad ways to watch a live strategy. <bookmark mark='a'/> Run a five percent test every month: over ten "
            "years you will raise a false alarm far more often than five percent of the time, because every look is "
            "another chance. <bookmark mark='b'/> Or look only once, after five years, and accept five years of losses "
            "from a strategy that died in the first. <bookmark mark='c'/> Part four built the third way: testing by "
            "betting. Bet against the strategy's claim. If the claim is true, your wealth is a nonnegative martingale, "
            "and Ville's inequality says it reaches one over alpha with probability at most alpha, however often you look."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def bet(self):
        rows = [cmath(r"H_0", r":", r"\ \mathbb{E}_{t-1}\, r_t \ \ge\ m", font_size=40, colors={r"H_0": BAD}),
                cmath(r"x_t", r"=", r"\frac{m - r_t}{4\,\hat\sigma}", font_size=40, colors={r"x_t": RULE}),
                cmath(r"E_t", r"=", r"\frac{1}{K}\sum_{j=1}^{K}\prod_{s \le t}\big(1 + \lambda_j x_s\big)", font_size=38,
                      colors={r"E_t": HURDLE}),
                cmath(r"\Pr\big(\sup_t E_t \ge 20\big)", r"\le", r"\tfrac{1}{20} = 5\%", font_size=38,
                      colors={r"\Pr\big(\sup_t E_t \ge 20\big)": GOOD})]
        whys = [why(r"the claim being monitored: the strategy still earns $m$ a month, its backtest mean (or some "
                    r"fraction of it)"),
                why(r"the shortfall each month, scaled by four in-sample standard deviations (and winsorised there, "
                    r"about one month in a hundred), so that $|x_t| < 1$"),
                why(r"a gambler who bets a fixed fraction $\lambda_j \in \{0.1, \dots, 0.95\}$ of wealth that returns will "
                    r"fall short, mixed over $K$ fractions: under $H_0$ each product has mean at most one, so $E$ is an "
                    r"e-process"),
                why(r"Ville's inequality: whenever the monitor is read, the chance it ever passes 20 when the claim is "
                    r"true is at most 5\%")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.5, buff=0.3, edge=6.9)
        with self.voiceover(
            "The monitor the House runs. <bookmark mark='a'/> The claim: the strategy still earns m a month, its backtest "
            "mean, or some fraction of it. <bookmark mark='b'/> Each month, measure the shortfall, m minus the return, "
            "scaled so that it lies between minus one and one. <bookmark mark='c'/> Bet a fixed fraction of wealth "
            "that the strategy will fall short, and mix several fractions so that no single choice of bet size has to "
            "be right. If the claim is true, every one of these bets loses on average, and the mixture is an e-process. "
            "<bookmark mark='d'/> When it passes twenty, the claim is rejected at five percent, and that holds however "
            "many months you looked."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def example(self, ex, col):
        x = _years(ex["ym"])
        cum = np.asarray(ex["cum"])
        bt = ex["m_in"] * np.arange(1, len(cum) + 1)
        path = np.asarray(ex["path"])
        lo1, hi1 = float(min(cum.min(), 0) - 1), float(max(cum.max(), bt.max()) + 1)
        g1 = axes([x[0], x[-1]], [lo1, hi1], x_length=5.6, y_length=3.4, xlabel=r"after publication",
                  ylabel=r"cumulative return, \%", xticks=[], yticks=[0], font_size=13).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.4)
        ax1 = g1.ax
        l_bt = DashedLine(ax1.c2p(x[0], bt[0]), ax1.c2p(x[-1], bt[-1]), color=IS_C, stroke_width=2)
        l_cum = curve(ax1, x, cum, OOS_C, stroke_width=3)
        hi2 = max(2.5, float(path.max()) + 0.3)
        g2 = axes([x[0], x[-1]], [-2, hi2], x_length=5.4, y_length=3.4, xlabel=r"after publication",
                  ylabel=r"the monitor, $\log_{10} E_t$", xticks=[], yticks=[-2, 0, 2], font_size=13).to_edge(
            RIGHT, buff=0.5).shift(DOWN * 0.4)
        ax2 = g2.ax
        thr = DashedLine(ax2.c2p(x[0], np.log10(20)), ax2.c2p(x[-1], np.log10(20)), color=HURDLE, stroke_width=2)
        thr_l = label(r"20", font_size=14, color=HURDLE).next_to(ax2.c2p(x[-1], np.log10(20)), RIGHT, buff=0.08)
        l_e = curve(ax2, x, np.clip(path, -2, hi2), col, stroke_width=3)
        flag = None
        if ex.get("flag_full"):
            fy = ex["flag_full"] // 100 + (ex["flag_full"] % 100 - 0.5) / 12
            flag = Dot(ax2.c2p(fy, np.log10(20)), color=BAD, radius=0.08)
        name = ex["long"]
        head = VGroup(label(rf"{name}", font_size=26, color=col),
                      MathTex(rf"\text{{published}}\ {ex['year']},\ \ t = {ex['t_in']:.1f}\ \text{{in its paper's sample}}",
                              font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.35)
        foot = MathTex(rf"\text{{backtest}}\ {ex['m_in']:.2f}\%\ \text{{a month}};\ \ \text{{after}}\ {ex['m_post']:.2f}\%"
                       rf"\ \text{{over}}\ {ex['n_post']}\ \text{{months}}", font_size=24).to_edge(DOWN, buff=0.3)
        flagged = flag is not None
        with self.voiceover(
            ("A predictor from the zoo of Part twenty-five: dividend seasonality, published in 2013, with an "
             "in-sample t-statistic above fourteen. <bookmark mark='a'/> The dashed line is what its backtest "
             "promised, a third of a percent a month; the solid line is what it earned after publication: almost "
             "nothing. <bookmark mark='b'/> The monitor's wealth, betting against the promise, rises as the shortfall "
             "accumulates, and crosses twenty in August 2018, five years in. From that month the claim that it still "
             "works is rejected, with an error rate that did not depend on how often anyone looked.")
            if flagged else
            ("And one that kept its promise: the predicted dividend yield, published in 1979. <bookmark mark='a'/> "
             "After publication it earned more than its backtest. <bookmark mark='b'/> The monitor's wealth drifts "
             "down, as a bet against a true claim should, and never comes near twenty. Forty years of monthly looking, "
             "no false alarm.")
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), Create(thr), FadeIn(thr_l))
            vo.wait_until("a")
            self.play(Create(l_bt), Create(l_cum), FadeIn(foot), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_e), run_time=2.5)
            if flag is not None:
                self.play(FadeIn(flag, scale=1.5))
        self.add(illustration(r"Open Source Asset Pricing 2024.10; the House's \texttt{martingale.EProcess}"))
        self.wait(0.4)
        self.clear_scene()

    def zoo(self, m):
        f, h = m["full"], m["half"]
        yrs = np.asarray(f["years_to_flag"])
        rows = VGroup(
            MathTex(rf"{m['n']}\ \text{{predictors with a positive backtest, monitored from publication to 2020}}",
                    font_size=28),
            MathTex(rf"H_0:\ \text{{as good as the backtest}}\ \Rightarrow\ {f['flagged']}\ \text{{flagged}},\ "
                    rf"{f['ebh']}\ \text{{by e-BH at 10\%}}", font_size=28, color=BAD),
            MathTex(rf"H_0:\ \text{{at least half the backtest}}\ \Rightarrow\ {h['flagged']}\ \text{{flagged}},\ "
                    rf"{h['ebh']}\ \text{{by e-BH}}", font_size=28, color=HURDLE),
            MathTex(rf"\text{{median time to flag}}:\ {np.median(yrs):.0f}\ \text{{years after publication}}", font_size=26,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.35).shift(UP * 0.5)
        foot = wrapped_label(r"each flag is anytime-valid at 5\% for its own predictor; e-BH (Wang and Ramdas 2022) turns the "
                             r"final e-values into a list whose false discovery rate is at most 10\% under any dependence "
                             r"between predictors. The monitor can tell `not as advertised' within years, and `not even "
                             r"half' only slowly", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the whole zoo. <bookmark mark='a'/> Two hundred and seven published predictors with a positive "
            "backtest, each monitored from its publication to 2020. Against the claim that each is as good as its "
            "backtest, sixty-eight are flagged, and forty survive e-BH, the e-value version of the false discovery "
            "rate, at ten percent. <bookmark mark='b'/> Against the weaker claim, at least half as good, only seven "
            "are flagged. The median flag comes eight years after publication. <bookmark mark='c'/> That is the honest "
            "speed of evidence. A monitor can tell you within years that a strategy is not what its backtest "
            "promised; it takes far longer to tell you it is not even half of it, because a Sharpe ratio is that hard "
            "to measure."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a live strategy's monitor stands at 12 after three years, below the threshold of 20. A colleague "
                r"proposes switching to a 90\% test, threshold 10, so it can be stopped now. What is wrong with that?")
        with self.voiceover(
            "Pause and predict. A live strategy's monitor stands at twelve after three years, below its threshold of "
            "twenty. A colleague proposes switching to a ninety percent test, with a threshold of ten, so that it can be "
            "stopped today. What is wrong with that?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
