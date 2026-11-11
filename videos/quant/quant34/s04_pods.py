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
        self.add(c)
        with self.voiceover('Chapter three. A multi-manager platform combines teams, shared financing and firm-level risk decisions. We use a stipulated simulation to examine drawdown rules, replacement and compensation. Its arithmetic is informative under its assumptions; it does not calibrate a real platform.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pod(self):
        rows = [cmath(r"\text{a pod}", r"=", r"\text{a manager} + \text{analysts} + \text{a risk budget}", font_size=34,
                      colors={r"\text{a pod}": PM_C}),
                cmath(r"\text{the centre}", r":", r"\text{capital, financing, execution, risk, hedging}", font_size=32,
                      colors={r"\text{the centre}": PLAT_C}),
                cmath(r"\text{the book}", r"=", r"\textstyle\sum_{\text{pods}} \text{positions with measured covariance}",
                      font_size=32)]
        whys = [why(r"each team runs its own strategy, usually market-neutral, in its own sector or style, with a volatility "
                    r"budget rather than a dollar limit"),
                why(r"the platform finances the positions, executes, measures every pod's factor exposure and hedges what "
                    r"the pods share"),
                why('diversification depends on covariance, costs, funding and constraints; similar holdings can concentrate the firm instead')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The structure. <bookmark mark='a'/> A pod combines a manager, analysts and a risk budget; mandates vary. <bookmark mark='b'/> The centre may provide capital, financing, execution, measurement and shared hedges. <bookmark mark='c'/> The firm owns the sum of positions and their covariance. Many teams do not automatically create independent edges: shared factors, crowded exits and funding can concentrate risk."
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
        self.add(card)
        with self.voiceover(
            "A dated reported example. <bookmark mark='a'/> The Wall Street Journal reported in 2024 that at Millennium a five-percent drawdown could lead to halved capital and seven and a half percent to departure. Treat this as a historical reported description, not a universal or current contract. The simulation borrows those numerical thresholds, with its own explicit monthly monitoring and replacement rules."
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
                    r"capital normalization"),
                why(r"the depth of the stop in the research chapter's units is the stop over the budget: here "
                    r"$\delta = 1.5$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "A simplified proportional exposure calculation. <bookmark mark='a'/> Specify strategy volatility per unit exposure using the same capital denominator as the risk budget, and assume linear scaling. <bookmark mark='b'/> A billion dollars of capital, a five-percent annual risk budget and eight-percent strategy volatility then imply a scale of five eighths, or six hundred and twenty-five million dollars in that normalization. This is not a capacity estimate or a universal gross-notional rule. <bookmark mark='c'/> A seven-and-a-half-percent stop is one and a half annual volatility units deep. Known drift, monitoring and the time unit also enter its model lifetime."
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
                why('pass-through costs can be several percent a year; this chosen comparison depends on gross returns, cost definitions and fee terms; a stop does not guarantee steady profits')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""A single-period fee illustration. <bookmark mark='a'/> Fifteen percent gross, a two-percent capital fee, then twenty percent of remaining profit leaves {100*fund:.1f} percent. <bookmark mark='b'/> Replace that capital fee with stipulated six-percent pass-through costs and the same profit share: {100*pt:.1f} percent remains. Assume positive eligible profit and no high-water mark or timing effects. <bookmark mark='c'/> At equal gross returns the larger cost reduces investor return. A platform would need other advantages to offset it; stops cannot guarantee a high or steady gross return."""
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
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The chosen simulation is not a real firm's record. <bookmark mark='a'/> Two hundred slots run for thirty years. Skill is either a fixed point five for every hire or an independent Normal draw with mean and standard deviation point five. <bookmark mark='b'/> Monthly arithmetic profit is observed before halving or firing; replacement is immediate, free and independently drawn. <bookmark mark='c'/> Positive calendar-year profit is paid at twenty percent, without a high-water mark or clawback. Firing resets that slot's running profit and payout accumulator. The common shock has correlation point one; year-end exposure restoration is another chosen rule."
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
        self.add(title, tab[0], tab[1], foot)
        with self.voiceover(
            f"""The heterogeneous-skill case averages eight fixed simulation seeds. <bookmark mark='a'/> At ten-percent annual volatility, about {fa:.0f} percent of slots are replaced per year; at five percent, {fb:.0f} percent. <bookmark mark='b'/> Investor annual-return Sharpe averages {sb:.2f} with the five-percent rule, versus {sc:.2f} without stops. The displayed uncertainty is the across-seed standard deviation with population normalization divided by root eight, not a real-market confidence interval. Selection, time-varying exposure, free replacement and payout resets all contribute; this comparison does not isolate one cause."""
        ) as vo:
            self._show(vo, title, tab, foot)
        self.wait(0.4)
        self.clear_scene()

    def table_same(self, p):
        title, tab, foot = self._table(p, "0.0")
        b, c = p[f"{KEYS[1]} | skill sd 0.0"], p[f"{KEYS[2]} | skill sd 0.0"]
        sb, sc = b["investor_sharpe"], c["investor_sharpe"]
        self.add(title, tab[0], tab[1], foot)
        with self.voiceover(
            f"""Now every hire has the same stipulated skill. <bookmark mark='a'/> The drawdown rules still change exposure and payouts, despite no skill differences to select. <bookmark mark='b'/> The cached investor ratios are {sb:.2f} with stops and {sc:.2f} without. The stopped estimate is higher here; it does not show that stops cost a little. Each row's across-seed uncertainty is descriptive. We do not have a paired-difference uncertainty estimate, and cannot attribute this difference to manager selection."""
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
                cmath(r"\text{a stop}", r"=", r"\text{a rule requiring a null, deadline and calibration}", font_size=32)]
        whys = [why(r"the managers the rule fired had, on average, less true skill than a new hire"),
                why(r"after thirty years the seats are held by better managers than the hiring pool; without stops the "
                    r"pool's average stays where it was"),
                why('the research chapter reports simulated deadline stop frequencies; a hypothesis test requires a null, alternative and calibrated rejection rule')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Selection is visible within the stipulated model. <bookmark mark='a'/> Fired managers have average latent Sharpe {b['fired_skill']:.2f}, below the hiring mean point five. <bookmark mark='b'/> The final seated average is {b['final_skill']:.2f}, versus {c['final_skill']:.2f} without stops. These latent quantities are known to the simulator, not observed as true skill in practice. <bookmark mark='c'/> A stopping rule becomes a statistical test only after specifying its null, alternative, deadline and rejection rule. The research panel gives simulated stop probabilities, not an exact calibrated live-manager skill test."""
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
        self.add(rows[0], whys[0])
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
                          width=12.4, font_size=26),
            desk_question(r"protecting the strategy", r"non-compete clauses and garden leave; in 2024 Jane Street sued "
                          r"Millennium and two former traders over an Indian options strategy, and the case was settled "
                          r"later that year, as reported", width=12.4, font_size=26),
            desk_question(r"crowding inside the platform", r"many pods in one sector hold similar positions; the centre "
                          r"measures the overlap and hedges it, because a crowd inside the firm is still a crowd (Part 33)",
                          width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
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
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('C_1=C_2=100,\\quad (\\pi_1,\\pi_2)=(10,-10),\\quad B=0.2\\sum_i\\max(\\pi_i,0)', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Find bonus B, total investor P\\&L, investor return on capital 200, and bonus divided by gross P\\&L. Check the zero denominator.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. Two pods each have one hundred units of capital. One earns ten and the other loses ten. A bonus pays twenty percent of each positive profit. Find total bonus, investor profit and investor return on two hundred capital. Is bonus divided by gross profit defined?'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
