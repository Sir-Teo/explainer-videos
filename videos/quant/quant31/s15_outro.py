from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import (BAD, COST_C, FAC_C, GOOD, GP_C, HURDLE, IC_C, PART, REAL_C, SPEC_C, comma,
                                         load)

DESK = [
    (r"IC 0.05, 500 stocks, rebalanced monthly. Information ratio?",
     r"$0.05\sqrt{6000} \approx 3.9$ by the fundamental law; but if the monthly IC has a standard deviation of 0.10, the "
     r"research chapter gives $0.05/\sqrt{0.01 + 0.998/500} \approx 0.46$ a month, about 1.6 a year"),
    (r"A portfolio's bias statistic is 1.30 over two years of daily data. What does it mean?",
     r"realised volatility is 30\% above forecast, far outside the band $1 \pm 2\sqrt{2/504} \approx 1 \pm 0.13$: the "
     r"model under-forecasts this portfolio's risk"),
    (r"A book neutral to every factor forecasts 4\% volatility. How can it lose 10\% in a week?",
     r"through a common risk the model does not contain: crowded positions unwound by others (August 2007), a variance "
     r"forecast near zero (Chapter 11), or a factor that moved more than its history"),
    (r"A strategy nets 6\% at \$100m after 2\% costs. What does it net at \$400m?",
     r"costs per dollar grow like $\sqrt A$: 4\% at four times the size, so 8\% gross nets 4\%"),
    (r"Trading costs quadruple. How should a Garleanu--Pedersen trader respond?",
     r"trade about half as fast ($a/\lambda \approx \sqrt{\gamma/\lambda}$), and cut the weight of fast signals in the aim "
     r"further, since $1/(1 + \phi a/\gamma)$ falls as $a$ rises"),
    (r"After the failed envelope, the desk adds a variance floor and re-runs 2021--25: Sharpe 0.4. What does the Track "
     r"Record say?",
     r"nothing new about the holdout: those years have been seen, so the repaired rule is a new trial on research data; "
     r"it waits for data that did not exist when it was written"),
]

PROBLEMS = [
    r"IC 0.05, 500 stocks, monthly: the annual IR by the fundamental law, and with a monthly IC standard deviation of "
    r"0.10.",
    r"Over two years of daily data, the 95\% band for the bias statistic; is 1.30 inside it?",
    r"Vasicek: $\hat\beta = 1.8$, standard error 0.3; true betas have mean 1.0 and sd 0.3. The posterior beta.",
    r"A strategy nets 6\% at \$100m after 2\% costs, under the square-root law: its net return at \$400m.",
    r"It breaks even at \$900m: the profit-maximising size, and the investors' share of the gross return there.",
    r"Show $a/\lambda \to \sqrt{\gamma/\lambda}$ as $\rho \to 0$ and $\lambda \gg \gamma$; what happens to the trade rate "
    r"when costs quadruple?",
    r"Two signals with IC 0.04, correlation 0.5: the IC of their best combination.",
    r"Two signals with daily decay rates 0.02 and 0.32: the ratio of their books' turnover.",
    r"A fund returned 12\%; its average beta was 0.4, the market returned 20\%, and the timing term was 2\%: selection.",
    r"A monthly IC with mean 0.03 and sd 0.06: the largest annual IR any breadth can give, and $N^*$.",
    r"(qual) Prove that in the model of the research chapter, $IR = \mu/\sqrt{\sigma^2(1 - 1/N) + (1 - \mu^2)/N}$; show "
    r"it increases in $N$ toward $\mu/\sigma$, and that $IR(N^*) \approx \mu/(\sigma\sqrt2)$ at $N^* = (1-\mu^2)/\sigma^2$.",
    r"(qual) For the scalar Garleanu--Pedersen problem, guess $V(x, f) = -\frac12 A_{xx}x^2 + A_{xf}xf - \frac12 A_{ff}f^2$; "
    r"derive the Riccati equation for $A_{xx}$, show the policy trades a fraction $a/\lambda$ toward an aim, and that the "
    r"aim's loading on a signal decaying at rate $\phi$ is $1/(1 + \phi a/\gamma)$ of Markowitz's.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("law"), load("model"), load("vasicek"), load("costs"), load("gp"), load("combine"),
                   load("attribution"), load("quake"), load("envelope"), load("theory"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, l, m, v, c, g, cb, a, q, e, th):
        cur = {r["aum"]: r["sharpe"] for r in c["curve"]}
        r32 = g["rows"][-1]
        mined = [r for r in th["coins"] if r["signal"] == "mined"][0]
        per = RM.ir_time_varying(0.05, 0.10, 500) * math.sqrt(12)
        items = [
            (rf"the fundamental law: $IR = TC\cdot IC\sqrt{{BR}}$; long only transfers {l['tc_long_only']:.2f}", IC_C),
            (rf"factor risk models: $X F X^\top + \Delta$; on the coins, {100 * m['fac_share']:.0f}\% of risk is common", FAC_C),
            (rf"the bias statistic: forecasts tested, {m['bias']['equal-weighted coins'][0]:.2f} for the equal-weighted coins",
             FAC_C),
            (rf"Vasicek's betas: error {v['mse']['raw']:.3f} $\to$ {v['mse']['shrunk']:.3f}", SPEC_C),
            (rf"the square-root law: \$1 million costs {100 * c['cost_1m']:.1f}\% in the median coin", COST_C),
            (rf"capacity: Sharpe {c['gross_sharpe']:.2f} gross, {cur[1e5]:.2f} at \$100k, {cur[1e6]:.2f} at \$1m", COST_C),
            (rf"Garleanu--Pedersen: at $\lambda = 32$, {r32['gp']:.2f} against myopic {r32['myopic']:.2f}", GP_C),
        ]
        items2 = [
            (r"multi-period optimisation: plan far, trade one step, re-plan", GP_C),
            (rf"combination: the regression {cb['combos']['ridge 0']['valid']:.3f} in 2020, equal weights "
             rf"{cb['combos']['equal']['valid']:.3f}", HURDLE),
            (r"capacity at $\frac49$ of break-even; Berk and Green: investors earn no alpha", HURDLE),
            (rf"August 2007: {100 * q['aug']['20070808']:.2f}\% and {100 * q['aug']['20070809']:.2f}\% in two days on the "
             r"industries", BAD),
            (rf"attribution: the mined alpha {100 * a['var_share_factor']:.0f}\% factor, specific Sharpe "
             rf"{a['sharpe_specific']:.2f}", SPEC_C),
            (rf"the envelope: {e['res']['gp']['sr_hold']:.2f}, from variances near zero; counter {comma(e['trials'])}", BAD),
            (rf"research: $IR = \mu/\sqrt{{\sigma^2 + (1 - \mu^2)/N}}$; the hook's 3.87 is {per:.2f}", REAL_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 31 in fourteen lines")
        with self.voiceover(
            "Part thirty-one in fourteen lines. The fundamental law turns skill and breadth into an information ratio, "
            "and the transfer coefficient charges for constraints. A factor risk model forecasts the covariance of many "
            "assets from a few factors and a diagonal; on the coins, most risk is common, and the bias statistic tests "
            "the forecasts. Vasicek's shrinkage improves betas. The square-root law prices every trade, and it gives "
            "every strategy a capacity. Garleanu and Pedersen's trader aims in front of the target and moves partway, "
            "and survives costs the myopic trader cannot."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 31 in fourteen lines")
        with self.voiceover(
            "Multi-period optimisation keeps the idea without the closed form. Combining signals by regression lost to "
            "simple weights out of sample. Capacity is a choice, and Berk and Green explain why investors do not see "
            "the skill. August 2007 showed what a shared risk model cannot see. Attribution showed the mined alpha was "
            "mostly a factor. The registered rule failed through variances near zero. And the research chapter proved "
            "exactly how much a moving IC costs."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. An IC of five percent across five hundred stocks, monthly: the law says three point "
            "nine, and a wandering IC says about one point six. <bookmark mark='a'/> A bias statistic of one point three "
            "means the model under-forecasts that portfolio's risk by thirty percent. <bookmark mark='b'/> A "
            "factor-neutral book can lose ten percent in a week through a risk its model does not contain."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "At four times the size, costs per dollar double. <bookmark mark='a'/> When costs quadruple, trade half as "
            "fast and lean further toward slow signals. <bookmark mark='b'/> And a rule repaired after seeing the sealed "
            "years is a new trial on data that is no longer sealed. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: the hook's information ratio; the bias statistic's band; a Vasicek beta; costs at four "
            "times the size; the profit-maximising size; the trade rate's limit; combining two signals; turnover from "
            "decay; attribution by hand; and the ceiling on an information ratio. Then two qualifying-exam problems: the "
            "theorem of the research chapter, and Garleanu and Pedersen's solution from the Riccati equation. "
            "Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"trend, carry and risk parity across asset classes, traded with costs", [32]),
            (r"the firm: capacity, fees, and who keeps the alpha", [33]),
            (r"market impact derived; execution scheduled", [37]),
            (r"crowding, liquidity spirals and crises", [41]),
            (r"the finale: every row, deflated", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-two trades trend and carry across asset classes with this part's costs and "
            "risk model. Part thirty-three is the firm, where capacity and fees decide who keeps the alpha. Part "
            "thirty-seven derives the square-root law and schedules the trades. Part forty-one returns to crowding and "
            "liquidity spirals. And the finale deflates every row."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Grinold and Kahn, \textit{Active Portfolio Management} (2nd ed., 2000); Isichenko, "
             r"\textit{Quantitative Portfolio Management} (2021); Paleologo, \textit{The Elements of Quantitative "
             r"Investing}; Narang, \textit{Inside the Black Box}; Boyd et al., \textit{Multi-Period Trading via "
             r"Convex Optimization} (2017)"],
            [r"Blume (1971, 1975); Vasicek (1973); Rosenberg (1974); Chen, Roll and Ross (1986); Connor and Korajczyk "
             r"(1986); Brinson, Hood and Beebower (1986); Perold (1988); Grinold (1989); Connor (1995); Torre (1997); "
             r"Almgren and Chriss (2000); Clarke, de Silva and Thorley (2002); Berk and Green (2004); Buckle (2004); Qian "
             r"and Hua (2004); Almgren, Thum, Hauptmann and Li (2005)",
             r"Khandani and Lo (2007, 2011); Ding (2010); T\'oth et al.\ (2011); Garleanu and Pedersen (2013); Lou and "
             r"Polk (comomentum); Berk and van Binsbergen (2015); Novy-Marx and Velikov (2016); Ding and Martin (2017); "
             r"Frazzini, Israel and Moskowitz (2018). Data: Binance's public market data; Kenneth French's data library"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Blume and Vasicek on betas to AQR's "
            "measurement of its own costs. Every number on screen was computed by the House's code from Binance's public "
            "market data and Kenneth French's industry portfolios, with simulations and illustrations labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("portfolio",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 32, Systematic Macro and Alternative Premia", font_size=30, color=QC.IDEA
                    ).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House's portfolio and risk desk now has a risk model, a cost model and a trading rule, and two guards it "
            "learned the hard way. <bookmark mark='a'/> Next, Part thirty-two: systematic macro and alternative premia. "
            "Trend following across a century, volatility targeting, and carry, value and defensive premia as one book."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
