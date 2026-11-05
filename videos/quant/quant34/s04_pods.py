from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PLAT_C, PM_C, STOP_C, fit_right, load

KEYS = ["10% vol, halve 5%, cut 7.5%", "5% vol, halve 5%, cut 7.5%", "5% vol, no stops"]


class Pods(VoiceoverScene):
    def construct(self):
        p = load("platform")
        self.card()
        self.pod()
        self.rules()
        self.sizing()
        self.passthrough()
        self.setup_()
        self.table_var(p)
        self.selection(p)
        self.table_same(p)
        self.netting(p)
        self.talent()
        self.question()

    def card(self):
        c = chapter_card(3, r"The pod model", r"How does a platform give capital to traders, and take it back?", part=PART)
        with self.voiceover("Chapter three. The fastest-growing kind of hedge fund in the last decade is the platform: "
                            "a central firm that hires hundreds of small teams, gives each a slice of capital, and takes "
                            "it back by rule. Its arithmetic is the arithmetic of drawdown stops."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pod(self):
        rows = [cmath(r"\text{a pod}", r"=", r"\text{a manager} + \text{analysts} + \text{a risk budget}", font_size=34,
                      colors={r"\text{a pod}": PM_C}),
                cmath(r"\text{the centre}", r":", r"\text{capital, financing, execution, risk, hedging}", font_size=32,
                      colors={r"\text{the centre}": PLAT_C}),
                cmath(r"\text{the book}", r"=", r"\textstyle\sum_{\text{pods}} \text{small, nearly independent edges}",
                      font_size=32)]
        whys = [why(r"each team runs its own strategy, usually market-neutral, in its own sector or style, with a volatility "
                    r"budget rather than a dollar limit"),
                why(r"the platform finances the positions, executes, measures every pod's factor exposure and hedges what "
                    r"the pods share"),
                why(r"Part 31's breadth: many weakly correlated pods make a book with a much higher Sharpe ratio than any "
                    r"one of them")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The structure. <bookmark mark='a'/> A pod is a manager, a few analysts and a risk budget, usually set in "
            "volatility rather than dollars. <bookmark mark='b'/> The centre provides the capital, the financing, the "
            "execution and the risk system, and hedges the factor exposures the pods share. <bookmark mark='c'/> The "
            "book is a sum of many small, nearly independent edges: Part thirty-one's breadth, organised as a business."
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

    def rules(self):
        card = firm_card(r"Drawdown rules, as reported", r"the Wall Street Journal reported in 2024 that at Millennium a "
                         r"portfolio manager who loses 5\% from the peak can have their capital halved, and at 7.5\% may "
                         r"be let go; Part 8 built the drawdown floor; here the question is how often such a rule fires",
                         numbers=((r"5\% / 7.5\%", r"halve / cut, as reported"),), kind=r"The rule", width=10.6,
                         font_size=22).move_to(UP * 0.4)
        with self.voiceover(
            "The rule that makes it work. <bookmark mark='a'/> The Wall Street Journal reported in 2024 that at "
            "Millennium a manager who loses five percent from their peak can have their capital halved, and at seven "
            "and a half percent may be let go. Part eight built a drawdown floor for one investor. Here the question is "
            "how often such a rule fires, and what it does to a firm of hundreds of managers."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def sizing(self):
        budget, svol = 0.05, 0.08
        L = budget / svol
        cap = 1e9
        rows = [cmath(r"\text{notional}", r"=", r"\text{capital} \times \frac{\text{volatility budget}}{\text{strategy volatility}}",
                      font_size=32, colors={r"\text{notional}": PM_C}),
                cmath(r"\$1\text{bn},\ 5\%\ \text{budget},\ 8\%\ \text{strategy}", r"\Rightarrow",
                      rf"\${cap * L / 1e6:.0f}\text{{m}}\ \text{{of risk-weighted positions}}", font_size=28),
                cmath(r"\text{stop}", r"=", r"7.5\% \text{ of capital} = 1.5\ \text{budgets}", font_size=32,
                      colors={r"\text{stop}": STOP_C})]
        whys = [why(r"a pod is given capital and a volatility budget; its positions are scaled so the forecast volatility "
                    r"of its P\&L, in percent of capital, equals the budget"),
                why(r"a market-neutral strategy whose unscaled volatility is 8\% runs at five eighths of its notional "
                    r"capacity"),
                why(r"the depth of the stop in the research chapter's units is the stop over the budget: here "
                    r"$\delta = 1.5$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How a pod is sized. <bookmark mark='a'/> It is given capital and a volatility budget, and its positions are "
            "scaled so the forecast volatility of its profit equals the budget. <bookmark mark='b'/> A billion dollars, "
            "a five percent budget, and a strategy whose own volatility is eight percent: the pod runs five eighths of a "
            "billion in risk-weighted positions. <bookmark mark='c'/> And the stop, seven and a half percent of capital, "
            "is one and a half budgets deep. That ratio, not the stop itself, is what the research chapter shows decides "
            "how long the pod lasts."
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

    def passthrough(self):
        g, c, pf, mf = 0.15, 0.06, 0.20, 0.02
        pt = (g - c) * (1 - pf)
        fund = (g - mf) * (1 - pf)
        rows = [cmath(r"\text{classic}", r":", rf"(g - 2\%)(1 - 20\%) = {100 * fund:.1f}\%", font_size=34),
                cmath(r"\text{pass-through}", r":", rf"(g - \text{{costs}})(1 - 20\%) = {100 * pt:.1f}\%", font_size=34,
                      colors={r"\text{pass-through}": PLAT_C}),
                cmath(r"g = 15\%,\ \text{costs} = 6\%", r"\Rightarrow", r"\text{the platform must earn more, gross}",
                      font_size=30)]
        whys = [why(r"a classic fund: a fixed management fee, then a fifth of the profit"),
                why(r"a platform passing through its costs, including what it pays the pods, then a fifth of the profit, as "
                    r"reported for several large platforms"),
                why(r"pass-through costs can be several percent a year; the model works only if the gross return is high "
                    r"and steady")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How investors pay. <bookmark mark='a'/> A classic fund takes a fixed fee, say two percent, then a fifth of "
            f"the profit: on a fifteen percent gross return, {100 * fund:.1f} percent is left. <bookmark mark='b'/> A "
            "platform that passes through its costs, including what it pays the pods, and then takes a fifth: with six "
            f"percent of costs, {100 * pt:.1f} percent. <bookmark mark='c'/> The pass-through model works only if the "
            "gross return is high and steady, which is exactly what the stops are for."
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

    def setup_(self):
        rows = [cmath(r"S_i", r"\sim", r"N(0.5,\ 0.5^2)\ \ \text{or}\ \ S_i = 0.5", font_size=34, colors={r"S_i": PM_C}),
                cmath(r"\text{rules}", r":", r"\text{halve at } 5\%,\ \text{cut at } 7.5\%;\ \text{replace the cut}",
                      font_size=32, colors={r"\text{rules}": STOP_C}),
                cmath(r"\text{pay}", r"=", r"20\% \text{ of each pod's positive year};\ \rho = 0.1", font_size=32)]
        whys = [why(r"200 seats for 30 years; each manager's true Sharpe ratio drawn at hiring, unknown to the platform, "
                    r"either varying across managers or the same for all"),
                why(r"monthly P\&L at 10\% or 5\% volatility; the drawdown rules as reported; a fired manager is "
                    r"replaced by a new draw"),
                why(r"each pod is paid on its own year, with no netting against losers; the pods share a common shock with "
                    r"correlation 0.1")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The simulation. <bookmark mark='a'/> Two hundred seats for thirty years. Each manager's true Sharpe ratio "
            "is drawn when they are hired and unknown to the platform: either it varies across managers, around one "
            "half, or every manager has exactly one half. <bookmark mark='b'/> Monthly profit and loss at ten or five "
            "percent volatility, halved at five percent down, cut at seven and a half, and every cut manager replaced. "
            "<bookmark mark='c'/> Each pod is paid a fifth of its own positive years, with no netting against the "
            "losers, and the pods share a common shock."
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

    def _table(self, p, sd):
        hx = [-4.4, -1.6, 0.6, 2.8, 5.0]
        head = VGroup(label(r"pods' volatility and rules", font_size=16, color=GREY_B),
                      label(r"gross, \% a year", font_size=16, color=GREY_B),
                      label(r"investors' Sharpe", font_size=16, color=GOOD), label(r"fired a year", font_size=16,
                                                                                   color=STOP_C),
                      label(r"paid to pods", font_size=16, color=GREY_B))
        tab = VGroup(head)
        for k in KEYS:
            r = p[f"{k} | skill sd {sd}"]
            tab.add(VGroup(label(k.replace("%", r"\%"), font_size=17), MathTex(f"{100 * r['gross_mean']:.1f}", font_size=24),
                           MathTex(rf"{r['investor_sharpe']:.2f} \pm {r['investor_sharpe_se']:.2f}", font_size=22),
                           MathTex(rf"{100 * r['fired_per_year']:.0f}\%", font_size=24),
                           MathTex(rf"{100 * r['payout_share']:.0f}\%", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        title = label(r"skill varies across managers" if sd == "0.5" else r"every manager has the same skill",
                      font_size=26, color=PM_C).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"simulated: 200 seats, 30 years, 8 runs averaged ($\pm$ one standard error); paid to pods is "
                             r"the share of the platform's gross P\&L; illustration, not any firm's numbers", 11.4, 15,
                             GREY_A).to_edge(DOWN, buff=0.5)
        return title, tab, foot

    def _show(self, vo, title, tab, foot):
        self.play(FadeIn(title), FadeIn(tab[0]), FadeIn(foot))
        vo.wait_until("a")
        self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[3])) for r_ in tab[1:]], lag_ratio=0.25))
        vo.wait_until("b")
        self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[4])) for r_ in tab[1:]], lag_ratio=0.25))

    def table_var(self, p):
        title, tab, foot = self._table(p, "0.5")
        a, b, c = (p[f"{k} | skill sd 0.5"] for k in KEYS)
        fa, fb = 100 * a["fired_per_year"], 100 * b["fired_per_year"]
        sb, sc = b["investor_sharpe"], c["investor_sharpe"]
        with self.voiceover(
            "When skill varies. <bookmark mark='a'/> At ten percent volatility the rules fire constantly: "
            f"{fa:.0f} percent of seats a year. At five percent, {fb:.0f} percent. <bookmark mark='b'/> And the stops "
            f"pay: with them, the investors' Sharpe ratio is {sb:.2f}; without them, {sc:.2f}. The rule replaces "
            "managers who are losing with new draws, and the losers are, more often than not, the ones without skill."
        ) as vo:
            self._show(vo, title, tab, foot)
        self.wait(0.4)
        self.clear_scene()

    def table_same(self, p):
        title, tab, foot = self._table(p, "0.0")
        b, c = p[f"{KEYS[1]} | skill sd 0.0"], p[f"{KEYS[2]} | skill sd 0.0"]
        sb, sc = b["investor_sharpe"], c["investor_sharpe"]
        with self.voiceover(
            "When every manager has the same skill. <bookmark mark='a'/> The rules fire as often, because a drawdown is "
            "mostly luck. <bookmark mark='b'/> But now firing a manager only replaces them with an identical one: the "
            f"investors' Sharpe ratio is {sb:.2f} with the stops and {sc:.2f} without, within a standard error or so of "
            "each other. A stop earns its keep as a test of skill that varies."
        ) as vo:
            self._show(vo, title, tab, foot)
        self.wait(0.4)
        self.clear_scene()

    def selection(self, p):
        b = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"]
        c = p["5% vol, no stops | skill sd 0.5"]
        rows = [cmath(r"\bar S_{\text{fired}}", r"=", rf"{b['fired_skill']:.2f}", font_size=38, colors={r"\bar S_{\text{fired}}": STOP_C}),
                cmath(r"\bar S_{\text{seated, year 30}}", r"=", rf"{b['final_skill']:.2f}\ \ (\text{{no stops: }}{c['final_skill']:.2f})",
                      font_size=34, colors={r"\bar S_{\text{seated, year 30}}": GOOD}),
                cmath(r"\text{a stop}", r"=", r"\text{a sequential test of } H_0: S \le 0", font_size=32)]
        whys = [why(r"the managers the rule fired had, on average, less true skill than a new hire"),
                why(r"after thirty years the seats are held by better managers than the hiring pool; without stops the "
                    r"pool's average stays where it was"),
                why(r"the research chapter computes the test's power exactly: how often a manager of each true Sharpe "
                    r"ratio is stopped")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why it works, measured. <bookmark mark='a'/> The managers the rule fired had an average true Sharpe ratio "
            f"of {b['fired_skill']:.2f}, below a new hire's one half. <bookmark mark='b'/> After thirty years the seats "
            f"are held by managers averaging {b['final_skill']:.2f}; without stops, {c['final_skill']:.2f}, the pool. "
            "<bookmark mark='c'/> A drawdown stop is a sequential test of whether a manager has skill, run on live money. "
            "The research chapter computes its power exactly."
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

    def netting(self, p):
        b = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"]
        rows = [cmath(r"\text{pay}", r"=", r"0.2 \textstyle\sum_i \max(\text{P\&L}_i, 0)", font_size=36),
                cmath(r"\text{platform P\&L}", r"=", r"\textstyle\sum_i \text{P\&L}_i", font_size=36),
                cmath(r"\text{share paid}", r"=", rf"{100 * b['payout_share']:.0f}\%\ >\ 20\%", font_size=36,
                      colors={r"\text{share paid}": BAD})]
        whys = [why(r"each pod is paid on its own profit; a losing pod pays nothing back"),
                why(r"the investors own the sum, losers included"),
                why(r"so the share of the platform's profit paid out exceeds the headline fifth: netting risk, a call "
                    r"option on every pod written by the investors")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And a cost the headline hides. <bookmark mark='a'/> Each pod is paid on its own profit, and a losing pod "
            "pays nothing back. <bookmark mark='b'/> The investors own the sum, losers included. "
            f"<bookmark mark='c'/> So the share of the platform's profit paid out is {100 * b['payout_share']:.0f} "
            "percent, not twenty: netting risk. The investors have written a call option to every pod. Part two priced "
            "the same call in a single fund's performance fee."
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

    def talent(self):
        cards = VGroup(
            desk_question(r"the market for managers", r"platforms compete for teams with guaranteed pay, sign-on payments "
                          r"and capital; a team's track record is its asset, and it walks out of the door every evening",
                          width=12.4, font_size=19),
            desk_question(r"protecting the strategy", r"non-compete clauses and garden leave; in 2024 Jane Street sued "
                          r"Millennium and two former traders over an Indian options strategy, and the case was settled "
                          r"later that year, as reported", width=12.4, font_size=19),
            desk_question(r"crowding inside the platform", r"many pods in one sector hold similar positions; the centre "
                          r"measures the overlap and hedges it, because a crowd inside the firm is still a crowd (Part 33)",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The people. <bookmark mark='a'/> Platforms compete for teams with guaranteed pay and capital, because a "
            "team's track record walks out of the door every evening. <bookmark mark='b'/> Firms protect strategies with "
            "non-compete clauses and garden leave, and with the courts: in 2024 Jane Street sued Millennium and two former "
            "traders over an Indian options strategy, and the case was settled later that year, as reported. "
            "<bookmark mark='c'/> And many pods in one sector end up holding similar positions, so the centre measures "
            "the overlap and hedges it: a crowd inside one firm is still a crowd."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two pods each run 10\% volatility with no skill. One makes 10\%, the other loses 10\%. The "
                       r"platform pays 20\% of each positive year. What share of the platform's P\&L is paid out?")
        with self.voiceover(
            "Pause and predict. Two pods each run ten percent volatility with no skill. One makes ten percent, the "
            "other loses ten. The platform pays a fifth of each positive year. What share of its profit does it pay out?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
