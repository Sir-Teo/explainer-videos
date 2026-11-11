from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, PART, PUT_C, SPY_C, fit_right, load


class Insurance(VoiceoverScene):
    def construct(self):
        v = load("shortvol")
        self.card()
        self.index()
        self.paths(v)
        self.table(v)
        self.decompose(v)
        self.windows(v)
        self.crisis()
        self.buyers()
        self.mirror()
        self.question()

    def card(self):
        c = chapter_card(7, r"Selling insurance", r"Which risk does an income stream hide?", part=PART)
        with self.voiceover(
            "Chapter seven. A variance risk premium compares matched variance claims under "
            "risk-neutral and physical expectations; it does not mean that every option is "
            "overpriced. We examine a published collateralised put-writing index. Its "
            "exposure includes equity risk, so its average return is not a pure measure "
            "of compensation for selling volatility."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def index(self):
        rows = [cmath(r"\text{benchmark}", r":", r"\text{monthly S\&P 500 cash-secured put writing}", font_size=31),
                cmath(r"r_{\rm toy}", r"=", r"r_f+p/K-\max(K-S_T,0)/K", font_size=36),
                label(r"one contract, initial collateral K, premium p held without interest", font_size=23)]
        step = ladder(self, rows, [
            why(r"Cboe PUT has specified strike, roll, settlement and Treasury-collateral rules"),
            why(r"chosen terminal accounting example; not the full daily index methodology"),
            why(r"broker margin, execution, premium reinvestment and funding must be specified separately")],
            keep=3, top=2.5, x=-0.3, align_index=None, buff=0.65, edge=6.9)
        with self.voiceover(
            "Cboe's PUT benchmark writes an approximately at-the-money one-month S and P "
            "five hundred put under specified roll and settlement rules. "
            "<bookmark mark='a'/> The displayed equation is a simpler chosen accounting "
            "example: initial collateral K earns the period risk-free rate, while premium "
            "p is held without interest. Subtract the terminal shortfall and divide by K. "
            "<bookmark mark='b'/> This explains asymmetry. It does not reproduce every "
            "daily index convention, and cash security does not settle an investor's broker "
            "requirements or execution costs. The strike need not equal the index level "
            "on every observation date."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def paths(self, v):
        md = np.asarray(v["months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        ys = {k: 100 * np.asarray(v["cum"][k], float) for k in ("put", "mkt")}
        lo = float(np.floor(min(y.min() for y in ys.values()) / 50) * 50)
        hi = float(np.ceil(max(y.max() for y in ys.values()) / 50) * 50)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4,
                 xlabel=r"2007--2020", ylabel=r"cumulative total return, \%",
                 xticks=[2008, 2012, 2016, 2020], yticks=[lo, 0, hi],
                 xfmt=lambda u: f"{u:.0f}", yfmt=lambda u: f"{u:.0f}", font_size=15
                 ).move_to(LEFT * 1.8 + DOWN * 0.2)
        lines = [curve(g.ax, x, ys[k], col, stroke_width=3)
                 for k, col in [("mkt", SPY_C), ("put", PUT_C)]]
        leg = legend([(SPY_C, r"French US market"), (PUT_C, r"Cboe PUT")], font_size=18
                     ).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        self.play(FadeIn(g), FadeIn(leg))
        with self.voiceover(
            "These one hundred sixty-seven months run from February 2007 through December "
            "2020. <bookmark mark='a'/> The comparison is Kenneth French's market series, "
            "rather than an exact copy of the underlying and settlement of each put. "
            "<bookmark mark='b'/> Both wealth paths compound total returns. PUT suffers "
            "large losses and recovers differently. A single short put has limited "
            "upside, but rolling contracts and collateral make a multi-period index "
            "more than one fixed terminal payoff. A benchmark path is also different "
            "from the realised returns of a fund paying fees and execution costs."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[1]), run_time=2)
        self.clear_scene()

    def table(self, v):
        p, m = v["put"], v["mkt"]
        rows = VGroup()
        for name, key, fmt in [(r"Sharpe", "sharpe", ".2f"), (r"annual SD", "vol", ".3f"),
                               (r"maximum drawdown", "maxdd", ".3f"), (r"monthly skew", "skew", ".2f")]:
            rows.add(label(f"{name}: market {m[key]:{fmt}}; PUT {p[key]:{fmt}}", font_size=27))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        foot = wrapped_label(r"Sharpe/SD/skew: monthly excess returns; drawdown: total NAV, "
                             r"first observed NAV as initial peak", 12.0, 19, GREY_A).to_edge(DOWN)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            f"PUT's annualised volatility is {100*p['vol']:.1f} percent and its Sharpe "
            f"{p['sharpe']:.2f}, against {100*m['vol']:.1f} percent and {m['sharpe']:.2f} "
            "for the market under these conventions. <bookmark mark='a'/> The reported "
            f"drawdowns are {100*p['maxdd']:.1f} and {100*m['maxdd']:.1f} percent. They "
            "start the running peak at the first observed net asset value, omitting a "
            "possible fall from an initial value of one. "
            f"<bookmark mark='b'/> PUT's monthly excess-return skewness is {p['skew']:.2f}. "
            "These are sample summaries. Square-root-of-twelve annualisation does not "
            "establish independent returns or identify a pure variance premium."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def decompose(self, v):
        rows = [cmath(r"\beta_{\rm proxy}", r"=", r"\frac{\operatorname{Cov}_{N-1}(r_P^e,r_M^e)}"
                      r"{\operatorname{Var}_N(r_M^e)}", font_size=37),
                cmath(r"\beta_{\rm proxy}", r"=", rf"{v['beta']:.3f},\quad "
                      rf"a_{{\rm proxy}}={100*v['alpha']:+.2f}\%\ \text{{annualised}}", font_size=35),
                label(r"covered-call decomposition motivates exposure questions; it is a different strategy",
                      font_size=22)]
        step = ladder(self, rows, [
            why(r"legacy covariance and variance use different divisors; this is not exact OLS"),
            why(r"12 times mean put excess minus beta proxy times mean market excess; no standard error"),
            why(r"Israelov--Nielsen (2015): distinguish equity, volatility and timing exposures")],
            keep=3, top=2.5, x=-0.3, align_index=None, buff=0.65, edge=6.9)
        with self.voiceover(
            "The original summary's beta is a proxy: covariance divides by N minus one, "
            "but variance divides by N. <bookmark mark='a'/> We display the convention "
            "rather than calling it exact OLS. Its annualised intercept subtracts this "
            "proxy times mean market excess return from mean put excess return. "
            "<bookmark mark='b'/> Without uncertainty estimates and a matched exposure "
            "model, this does not establish causal alpha or isolate option compensation. "
            "Israelov and Nielsen's covered-call decomposition distinguishes equity, "
            "volatility and timing. That framework motivates questions about option "
            "selling; it is not an identity for this series without the required parity "
            "and financing assumptions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.clear_scene()

    def windows(self, v):
        rows = VGroup()
        for key, window in [("2008", r"September--November 2008"), ("2020", r"February--March 2020")]:
            event = v["events"][key]
            rows.add(label(rf"{window}: PUT {100*event['put']:+.1f}\%, market {100*event['mkt']:+.1f}\%",
                           font_size=27))
        rows.arrange(DOWN, buff=0.6)
        foot = wrapped_label(r"selected historical windows; compounded total returns; neither label means a full year",
                             12.0, 19, GREY_A).to_edge(DOWN)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Window labels need dates. The first event is September through November "
            "2008, not the entire calendar year. <bookmark mark='a'/> The second is "
            "February through March 2020. The losses compound total returns over these "
            "selected intervals. Both series fall substantially. The comparison does "
            "not isolate volatility compensation or supply a prespecified crisis "
            "test. Applying either figure to its entire calendar year would be incorrect."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def crisis(self):
        card = crisis_card(r"5 February 2018", r"Volmageddon",
                           r"Credit Suisse's XIV tracked daily inverse short-term VIX futures; "
                           r"a greater-than-90\% indicative-value fall triggered termination. "
                           r"This was different from cash-secured PUT.", width=11.0, font_size=23)
        self.play(FadeIn(card))
        with self.voiceover(
            "The crisis file is February fifth, 2018. The VIX more than doubled and "
            "Credit Suisse's XIV suffered an indicative-value fall exceeding ninety "
            "percent, triggering termination. This is quoted event history. XIV's "
            "daily inverse VIX-futures exposure, reset and termination terms differed "
            "from cash-secured S and P put writing. Both illustrate hidden tail exposure, "
            "but their losses cannot be transferred between products by analogy."
        ):
            self.wait(0.2)
        self.clear_scene()

    def buyers(self):
        cards = VGroup(
            desk_question(r"demand", r"protection mandates, preferences and budgets can create hedging demand",
                          width=12.4, font_size=20),
            desk_question(r"intermediation", r"Garleanu--Pedersen--Poteshman (2009): imperfect hedging and dealer "
                          r"capacity can affect option prices relative to a benchmark", width=12.4, font_size=20),
            desk_question(r"testable mechanism", r"persistent demand does not guarantee a positive premium "
                          r"net of losses, capital, funding and execution", width=12.4, font_size=20)
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Who buys protection? Pension funds, insurers and structured-product desks "
            "can have mandates, preferences and budgets. <bookmark mark='a'/> Garleanu "
            "and coauthors study demand-based option pricing with imperfect hedging. "
            "Demand and dealer capacity can affect prices relative to a benchmark. "
            "<bookmark mark='b'/> This is not the same as comparing an undiscounted "
            "physical expected payoff with an option price. It is a mechanism to "
            "test; persistent demand alone cannot guarantee a premium after crash "
            "losses, funding, capital and execution."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def mirror(self):
        cards = VGroup(
            desk_question(r"put writing", r"negative skew and equity downside can coexist with apparently steady income",
                          width=12.4, font_size=20),
            desk_question(r"trend filters", r"sustained moves can help; reversals and jumps before exposure "
                          r"adjusts can defeat protection", width=12.4, font_size=20),
            desk_question(r"combination", r"weights, costs, horizon and joint tails decide protection; "
                          r"a payoff-shape analogy is insufficient", width=12.4, font_size=20)
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Compare payoff shapes carefully. Put writing has negative skew in this "
            "sample and substantial equity downside. <bookmark mark='a'/> Some trend "
            "filters benefit from sustained directional moves, yet lose on reversals "
            "or jumps before exposure adjusts. This is not an exact short-versus-long "
            "straddle replication. <bookmark mark='b'/> Ilmanen's survey discusses "
            "insurance compensation and lottery preferences. Combining two return "
            "shapes does not automatically buy protection. Portfolio weights, costs, "
            "horizon and joint tail outcomes determine the result."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('(r_1,\\ldots,r_{51})=(\\underbrace{1\\%,\\ldots,1\\%}_{50},-30\\%)', font_size=34),
            MathTex('\\overline r=\\frac{50(0.01)-0.30}{51}', font_size=34),
            MathTex('R_{\\rm compound}=1.01^{50}(0.70)-1', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"chosen returns: fifty months at +1\%, then one at -30\%; "
                       r"arithmetic mean and skewness sign?")
        self.play(FadeIn(q))
        with self.voiceover(
            "Pause and predict. A chosen sequence has fifty months at plus one percent "
            "and one month at minus thirty percent. The arithmetic mean is twenty "
            "percentage points divided by fifty-one, about point three nine two "
            "percent a month. The skewness is negative. That arithmetic average "
            "differs from the compound return, and positive average income alone "
            "does not describe the tail."
        ):
            self.wait(0.2)
        self.clear_scene()
