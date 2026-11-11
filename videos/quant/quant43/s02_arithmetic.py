from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, SKILL_C, fit_right,
                                         load)


class Arithmetic(VoiceoverScene):
    def construct(self):
        a = load("arith")
        self.card()
        self.identity()
        self.proof()
        self.costs(a)
        self.horizon(a)
        self.years_needed()
        self.fees(a)
        self.fee_compound()
        self.losers_game()
        self.scorecards()
        self.pedersen()
        self.grossman()
        self.question()

    def card(self):
        c = chapter_card(1, r"Sharpe's arithmetic", r"Can active managers, together, beat the market?", part=PART)
        with self.voiceover(
            "Chapter one, and the answer to the pause: exactly the market's return, before costs. Not roughly: "
            "exactly, for a common defined market with market-weighted passive holdings and a positive active share. William Sharpe called it the arithmetic of active management, and it needs no model of prices, "
            "no theory of efficiency and no data. It is accounting."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def identity(self):
        rows = [cmath(r"\text{market}", r"=", r"\text{passive} + \text{active}", font_size=42, colors={r"\text{market}": MKT_C}),
                cmath(r"\text{passive}", r":", r"\text{holds every security in market weights}", font_size=38),
                cmath(r"\Rightarrow", r"", r"r_{\text{passive}} = r_{\text{market}}", font_size=42),
                cmath(r"\Rightarrow", r"", r"r_{\text{active}} = r_{\text{market}}\ \ \text{(before costs)}", font_size=42,
                      colors={r"\Rightarrow": HURDLE})]
        whys = [why(r"every dollar in a security is held by someone, passive or active"),
                why(r"an index investor, by definition"),
                why(r"so passive investors earn the market return, before their (small) costs"),
                why(r"the market's return is the dollar-weighted average of the two, so active money in aggregate earns "
                    r"it too: Sharpe (1991)")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The argument. <bookmark mark='a'/> Every dollar invested in a market is held by someone, either passively "
            "or actively. <bookmark mark='b'/> A passive investor holds every security in its market weight. "
            "<bookmark mark='c'/> So passive money earns exactly the market's return. <bookmark mark='d'/> And because "
            "the market is the average of the two, active money, in aggregate, earns exactly the market's return too, "
            "before costs. Every active winner is matched, dollar for dollar, by an active loser."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"w_P\,r_P + w_A\,r_A", r"=", r"r_M,\qquad w_P + w_A = 1,\quad w_A>0", font_size=40),
                cmath(r"r_P = r_M", r"\Rightarrow", r"w_A\,r_A = (1 - w_P)\,r_M = w_A\,r_M", font_size=38),
                cmath(r"\Rightarrow", r"", r"r_A = r_M;\quad r_A - c_A < r_P - c_P \ \text{ if } c_A > c_P", font_size=38,
                      colors={r"\Rightarrow": GOOD})]
        whys = [why(r"the market's return is the value-weighted average of passive and active holdings"),
                why(r"substitute the passive return"),
                why(r"so after costs the average active dollar must trail the average passive dollar, by the difference "
                    r"in costs")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "In three lines. <bookmark mark='a'/> The market's return is the weighted average of passive and active "
            "returns. <bookmark mark='b'/> Put in the passive return, which is the market's. <bookmark mark='c'/> So "
            "the active return is the market's, and after costs the average active dollar trails the average passive "
            "one by exactly the difference in what they pay."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def costs(self, a):
        rows = [cmath(r"\text{active} - \text{index}", r"\sim", r"N\bigl(-cT,\ \sigma_{TE}^2 T\bigr)", font_size=42,
                      colors={r"\text{active} - \text{index}": ACT_C}),
                cmath(r"P(\text{beat})", r"=", r"\Phi\!\left(-\frac{c\sqrt T}{\sigma_{TE}}\right)", font_size=42,
                      colors={r"P(\text{beat})": HURDLE}),
                cmath(r"c = 1\%,\ \sigma_{TE} = 5\%", r":", r"\text{falls with every year}", font_size=38)]
        whys = [why(r"a manager with no skill: each year's active return has mean minus the cost and spread equal to "
                    r"the tracking error"),
                why(r"the chance the additive Gaussian cumulative active return is positive; not a general compounded-wealth probability"),
                why(r"costs accumulate linearly, luck only as the square root: time is on the index's side")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "So what does a manager with no skill look like? <bookmark mark='a'/> Each year it trails the index by its "
            "constant excess cost on average in this iid additive Gaussian example, with the stated tracking error. This sums active returns; it is not a general compounded-wealth calculation. <bookmark mark='b'/> The chance it is "
            "ahead after T years is this. <bookmark mark='c'/> Costs add up linearly in time, while luck grows only as "
            "the square root: the longer the horizon, the more the arithmetic wins."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def horizon(self, a):
        y = np.asarray(a["years"], float)
        th = np.asarray(a["theory"], float)
        sm = np.asarray(a["sim"], float)
        g = axes([0, 31], [0, 0.5], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"share of zero-skill managers ahead",
                 xticks=[0, 10, 20, 30], yticks=[0, 0.25, 0.5], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        yy = np.linspace(0.5, 30, 120)
        from scipy.stats import norm
        ln = curve(ax, yy, norm.cdf(-a["cost"] * np.sqrt(yy) / a["te"]), ACT_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.07, color=LUCK_C) for a_, b_ in zip(y, sm)])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(31, 0.5), color=GREY_C, stroke_width=1.5)
        leg = legend([(ACT_C, r"the formula"), (LUCK_C, r"20,000 simulated managers")], font_size=17)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        p1, p15, p30 = th[0], th[4], th[-1]
        with self.voiceover(
            "With a one percent cost and five percent tracking error. <bookmark mark='a'/> After one year, "
            f"{100 * p1:.0f} percent of zero-skill managers are ahead of the index: almost a coin toss. "
            f"<bookmark mark='b'/> After fifteen years, {100 * p15:.0f} percent; after thirty, {100 * p30:.0f}. "
            "<bookmark mark='c'/> Twenty thousand simulated managers sit on the formula. So a minority beating the "
            "index over fifteen years is what luck alone predicts: it is not, by itself, evidence of skill."
        ) as vo:
            self.play(FadeIn(g), FadeIn(half), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(ln, color=HURDLE))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in dots], lag_ratio=0.2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def years_needed(self):
        rows=[cmath(r"\text{signal-to-noise noncentrality}",r"\approx",r"\mathrm{IR}\sqrt T",font_size=37),
              cmath(r"\mathrm{IR}\sqrt T=2",r"\Rightarrow",r"T=(2/\mathrm{IR})^2",font_size=42),
              cmath(r"\mathrm{IR}=.5,.3,.2",r"\Rightarrow",r"T\approx16,44,100\ \text{years}",font_size=39)]
        whys=[why(r"iid stable annual Gaussian active returns with fixed mean and volatility; one pre-specified test"),
              why(r"a target signal-to-noise ratio, not a guarantee that the realised statistic exceeds two"),
              why(r"power also requires the alternative, critical value and error criterion; selection changes the problem")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=0,buff=.6)
        with self.voiceover(
            "How much information accumulates? <bookmark mark='a'/> In an iid stable Gaussian model, a test's "
            "signal-to-noise noncentrality grows like the information ratio times square-root years. "
            "<bookmark mark='b'/> Setting that quantity to two gives two over the information ratio, squared. "
            "<bookmark mark='c'/> The illustrative horizons are sixteen, forty-four and one hundred years. These "
            "are not guaranteed discovery dates or power calculations. At noncentrality two, a threshold near two "
            "still has power only around one half in a normal approximation. Multiple testing, changing skill and "
            "dependent returns require more than this scaling calculation."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def fees(self, a):
        rows = VGroup()
        for x in a["fee_grid"]:
            rows.add(VGroup(label(rf"cost {100 * x['cost']:.2f}\% a year", font_size=24, color=COST_C),
                            label(rf"ahead after 15 years: {100 * x['p15']:.0f}\%", font_size=24, color=ACT_C)
                            ).arrange(RIGHT, buff=0.8))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.3)
        note_ = wrapped_label(r"zero skill, 5\% tracking error; chosen constant excess costs in an additive Gaussian example",
                              10.0, 18, GREY_B).next_to(rows, DOWN, buff=0.5)
        g = a["fee_grid"]
        with self.voiceover(
            "And by cost. <bookmark mark='a'/> At a quarter of a percent a year, "
            f"{100 * g[0]['p15']:.0f} percent of zero-skill managers are still ahead after fifteen years. "
            f"<bookmark mark='b'/> At two percent, {100 * g[-1]['p15']:.0f}. The contractual percentage is an input here; dollar fees depend on assets and terms can change. Costs reduce expected "
            "returns under the model."
        ) as vo:
            self.play(FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def fee_compound(self):
        yrs = np.arange(0, 31)
        g = axes([0, 30], [1, 8.5], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"illustration: annual growth $1.07-f$",
                 xticks=[0, 10, 20, 30], yticks=[2, 4, 6, 8], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        fees = [(0.0005, MKT_C), (0.01, HURDLE), (0.02, COST_C)]
        lines = VGroup(*[curve(ax, yrs, (1.07 - f) ** yrs, col, stroke_width=3) for f, col in fees])
        ends = [(1.07 - f) ** 30 for f, _ in fees]
        leg = legend([(MKT_C, r"chosen cost 0.05\%"), (HURDLE, r"1\%"), (COST_C, r"2\%")], font_size=16)
        side = VGroup(leg, label(rf"after 30 years: {ends[0]:.1f}, {ends[1]:.1f}, {ends[2]:.1f}", font_size=17, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        e0, e1, e2 = ends
        lost = 100 * (1 - e2 / e0)
        with self.voiceover(
            "An illustrative fee convention subtracts f times beginning-of-year wealth from a constant seven percent annual gross gain; growth is one point zero seven minus f. <bookmark mark='a'/> One unit at a seven percent gross return for thirty years, at a "
            f"chosen cost of point zero five percent, becomes {e0:.1f}. <bookmark mark='b'/> At one percent a year, {e1:.1f}; at two, "
            f"{e2:.1f}: {lost:.0f} percent less wealth, for the same market. The certain part of a manager's return "
            "is the one that grows."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(side[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def losers_game(self):
        rows = [cmath(r"\text{gross}", r":", r"\text{a zero-sum game against other active money}", font_size=38,
                      colors={r"\text{gross}": ACT_C}),
                cmath(r"\text{net}", r":", r"\text{a negative-sum game, by the costs}", font_size=40, colors={r"\text{net}": COST_C}),
                cmath(r"\text{who wins}", r":", r"\text{information, risk exposures and luck all affect realised winners}", font_size=34)]
        whys = [why(r"relative to the market, every active gain is another active manager's loss"),
                why(r"fees, spreads, impact and taxes come out of the pool"),
                why(r"the accounting identity alone does not identify the cause of any individual winner")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "What the arithmetic makes of the game. <bookmark mark='a'/> Before costs, active management is zero-sum "
            "relative to the market: every gain is another active manager's loss. <bookmark mark='b'/> After costs, it "
            "is negative-sum. <bookmark mark='c'/> An individual winner may reflect information, risk exposures or luck; the identity does not identify its cause. Charles Ellis called active management the loser's game."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def scorecards(self):
        cards=VGroup(
            desk_question('SPIVA U.S. year-end 2024','reported 65\\% of active large-cap U.S. equity funds underperformed the S\\&P 500 in 2024',width=12.4,font_size=19),
            desk_question('a fund-count result',"category, horizon, benchmark, fees and survivorship methodology matter; this is not Sharpe's value-weighted identity",width=12.4,font_size=19),
            desk_question('skill inference',"an outperformance fraction alone does not identify each winner's true alpha",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("A dated empirical comparison. <bookmark mark='a'/> The SPIVA U.S. year-end twenty twenty-four report states that sixty-five percent of active large-cap U.S. equity funds underperformed the S and P five hundred in that year. <bookmark mark='b'/> This is a category-specific fund-count result with a stated benchmark and methodology, not the value-weighted holdings identity. Horizons, fees and treatment of closed or merged funds matter. <bookmark mark='c'/> A performance fraction alone does not identify each winning manager's true alpha or forecast the next period.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def pedersen(self):
        cards=VGroup(
            desk_question('Pedersen (2018)','issuance, repurchases and index changes require trading in a changing market portfolio',width=12.4,font_size=19),
            desk_question('the comparator','a real index fund need not maintain the complete market portfolio continuously or trade without frictions',width=12.4,font_size=19),
            desk_question('the conclusion','liquidity provision can have value; a conditional holdings identity is not contradicted by changing its premises',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("Pedersen sharpens the comparison. <bookmark mark='a'/> Issuance, repurchases and index changes make passive implementation a trading task. <bookmark mark='b'/> An index fund can differ from the complete market portfolio and face execution frictions; returns must be compared under those actual holdings and flows. <bookmark mark='c'/> Liquidity provision can then add value. This does not invalidate the conditional accounting identity. It changes the comparator and the economic assumptions, and it does not promise that every active manager earns the transfer.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def grossman(self):
        cards=VGroup(
            desk_question('Grossman and Stiglitz (1980)','under their costly-information assumptions, fully revealing prices would eliminate the incentive to pay for information',width=12.4,font_size=19),
            desk_question('equilibrium compensation',"the model balances information benefits and costs; this does not establish every manager's net alpha",width=12.4,font_size=19),
            desk_question('inference limit','an equilibrium mechanism is not evidence that a particular observed winner has skill',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("A model for why information is acquired. <bookmark mark='a'/> Grossman and Stiglitz show, under their costly-information assumptions, why fully revealing prices cannot support the incentive to become informed. <bookmark mark='b'/> Equilibrium compensation depends on their information and market structure; this is not a universal assertion that every manager earns exactly an information cost. <bookmark mark='c'/> The mechanism can motivate research questions, but a particular manager's skill still needs evidence. Pedersen's efficiently inefficient perspective develops related economic intuition.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def question(self):
        q = pause_card(r"two thousand funds, none with any skill, each measured over twenty years. How large is the best "
                       r"$t$-statistic for alpha among them?")
        with self.voiceover(
            "Pause and predict. Two thousand funds, none with any skill at all, each measured over twenty years. How "
            "large is the best t-statistic for alpha among them?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
