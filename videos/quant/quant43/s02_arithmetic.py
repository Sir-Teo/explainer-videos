from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
            "exactly. William Sharpe called it the arithmetic of active management, and it needs no model of prices, "
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
        rows = [cmath(r"w_P\,r_P + w_A\,r_A", r"=", r"r_M,\qquad w_P + w_A = 1", font_size=40),
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
                why(r"the chance its cumulative active return is positive after $T$ years"),
                why(r"costs accumulate linearly, luck only as the square root: time is on the index's side")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "So what does a manager with no skill look like? <bookmark mark='a'/> Each year it trails the index by its "
            "cost on average, and wanders around that by its tracking error. <bookmark mark='b'/> The chance it is "
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
        rows = [cmath(r"t", r"\approx", r"\text{IR}\,\sqrt T", font_size=44, colors={r"t": HURDLE}),
                cmath(r"t = 2", r"\Rightarrow", r"T = (2/\text{IR})^2", font_size=44),
                cmath(r"\text{IR} = 0.5,\ 0.3,\ 0.2", r"\Rightarrow", r"T = 16,\ 44,\ 100\ \text{years}", font_size=40,
                      colors={r"\Rightarrow": COST_C})]
        whys = [why(r"the $t$-statistic of an active return grows with the information ratio times the square root of "
                    r"the years observed"),
                why(r"to reach the usual two standard errors"),
                why(r"an information ratio of 0.5 is very good; most skilled managers, if any, have less, and their "
                    r"careers are shorter than the proof")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "How long would it take to tell? <bookmark mark='a'/> The t-statistic of a manager's active return grows "
            "with the information ratio times the square root of the years. <bookmark mark='b'/> To reach two standard "
            "errors takes two over the information ratio, squared. <bookmark mark='c'/> An excellent information ratio "
            "of a half needs sixteen years; a good one of nought point two needs a hundred. Most careers end before "
            "the proof does."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def fees(self, a):
        rows = VGroup()
        for x in a["fee_grid"]:
            rows.add(VGroup(label(rf"cost {100 * x['cost']:.2f}\% a year", font_size=24, color=COST_C),
                            label(rf"ahead after 15 years: {100 * x['p15']:.0f}\%", font_size=24, color=ACT_C)
                            ).arrange(RIGHT, buff=0.8))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.3)
        note_ = wrapped_label(r"zero skill, 5\% tracking error; an index fund's own cost is a few hundredths of a percent",
                              10.0, 18, GREY_B).next_to(rows, DOWN, buff=0.5)
        g = a["fee_grid"]
        with self.voiceover(
            "And by cost. <bookmark mark='a'/> At a quarter of a percent a year, "
            f"{100 * g[0]['p15']:.0f} percent of zero-skill managers are still ahead after fifteen years. "
            f"<bookmark mark='b'/> At two percent, {100 * g[-1]['p15']:.0f}. Fees are the one part of a manager's "
            "return that is certain."
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
        g = axes([0, 30], [1, 8.5], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"growth of 1 at a 7\% gross return",
                 xticks=[0, 10, 20, 30], yticks=[2, 4, 6, 8], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        fees = [(0.0005, MKT_C), (0.01, HURDLE), (0.02, COST_C)]
        lines = VGroup(*[curve(ax, yrs, (1.07 - f) ** yrs, col, stroke_width=3) for f, col in fees])
        ends = [(1.07 - f) ** 30 for f, _ in fees]
        leg = legend([(MKT_C, r"0.05\% a year, an index fund"), (HURDLE, r"1\%"), (COST_C, r"2\%")], font_size=16)
        side = VGroup(leg, label(rf"after 30 years: {ends[0]:.1f}, {ends[1]:.1f}, {ends[2]:.1f}", font_size=17, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        e0, e1, e2 = ends
        lost = 100 * (1 - e2 / e0)
        with self.voiceover(
            "And costs compound. <bookmark mark='a'/> One unit at a seven percent gross return for thirty years, at an "
            f"index fund's cost, becomes {e0:.1f}. <bookmark mark='b'/> At one percent a year, {e1:.1f}; at two, "
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
                cmath(r"\text{who wins}", r":", r"\text{whoever is better informed than the average active dollar}", font_size=34)]
        whys = [why(r"relative to the market, every active gain is another active manager's loss"),
                why(r"fees, spreads, impact and taxes come out of the pool"),
                why(r"so the relevant competition is not the index but the other professionals, and they improve")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "What the arithmetic makes of the game. <bookmark mark='a'/> Before costs, active management is zero-sum "
            "relative to the market: every gain is another active manager's loss. <bookmark mark='b'/> After costs, it "
            "is negative-sum. <bookmark mark='c'/> So the winners are those better informed than the average active "
            "dollar, and that average is set by other professionals, who keep improving. Charles Ellis called it the "
            "loser's game."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def scorecards(self):
        cards = VGroup(
            desk_question(r"what the scorecards show", r"for two decades, S\&P's scorecards have reported that most "
                          r"actively managed US equity funds trail their benchmarks over long horizons, after fees",
                          width=12.4, font_size=19),
            desk_question(r"what they do not show", r"whether the few that lead are skilled: Chapter 2's question", width=12.4,
                          font_size=19),
            desk_question(r"and survivorship", r"funds that close or merge, mostly poor performers, disappear from the "
                          r"average unless the data keep them: Part 26's bias, in the fund industry", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the data on real funds show. <bookmark mark='a'/> For two decades, S and P's scorecards have reported "
            "that most actively managed American equity funds trail their benchmarks over long horizons, after fees, "
            "as the arithmetic predicts. <bookmark mark='b'/> They cannot say whether the few that lead are skilled. "
            "<bookmark mark='c'/> And funds that close, mostly poor ones, vanish from averages unless the data keep them: "
            "Part twenty-six's survivorship bias, in the fund industry."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pedersen(self):
        cards = VGroup(
            desk_question(r"Pedersen (2018): the arithmetic's assumption", r"passive investors never trade; but the "
                          r"market changes: new issues, index additions and deletions, buybacks", width=12.4,
                          font_size=19),
            desk_question(r"so passive investors must trade", r"to stay at market weights they buy additions and sell "
                          r"deletions, at prices active traders can set", width=12.4, font_size=19),
            desk_question(r"and active management can add value", r"in aggregate, by supplying that liquidity and by "
                          r"making prices informative: the arithmetic bounds the average, not each manager", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Lasse Pedersen found the crack in the arithmetic. <bookmark mark='a'/> It assumes passive investors never "
            "trade. But the market changes: new shares are issued, companies join and leave indices. "
            "<bookmark mark='b'/> To stay at market weights, passive investors must buy what is added and sell what is "
            "removed, at prices active traders can set. <bookmark mark='c'/> So active management can add value in "
            "aggregate, by supplying that liquidity and making prices informative. The arithmetic bounds the average, "
            "not every manager."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def grossman(self):
        cards = VGroup(
            desk_question(r"Grossman and Stiglitz (1980)", r"if prices reflected all information, no one would pay to "
                          r"gather it, and then prices could not reflect it: a perfectly efficient market is impossible",
                          width=12.4, font_size=19),
            desk_question(r"the equilibrium", r"informed traders earn just enough to cover the cost of being informed; "
                          r"the market is efficiently inefficient, in Pedersen's phrase", width=12.4, font_size=19),
            desk_question(r"what it predicts", r"skill exists, earns about its cost, and is hardest to find where it "
                          r"is cheapest to copy", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the oldest answer to why anyone tries, from Part one. <bookmark mark='a'/> Sanford Grossman and Joseph "
            "Stiglitz: if prices reflected all information, no one would pay to gather it, and then they could not. "
            "<bookmark mark='b'/> In equilibrium, informed traders earn just enough to cover the cost of being "
            "informed: efficiently inefficient, in Pedersen's phrase. <bookmark mark='c'/> So skill should exist, earn "
            "about what it costs, and be hardest to find where it is cheapest to copy."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two thousand funds, none with any skill, each measured over twenty years. How large is the best "
                       r"$t$-statistic for alpha among them?")
        with self.voiceover(
            "Pause and predict. Two thousand funds, none with any skill at all, each measured over twenty years. How "
            "large is the best t-statistic for alpha among them?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
