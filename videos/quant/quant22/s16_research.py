from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, CARRY, GOOD, OIL, PART, load

PRICE, INV, SPR = OIL, QC.SPOT, QC.IMPLIED


class Research(VoiceoverScene):
    def construct(self):
        t = load("storage_public_example")
        self.card()
        self.equilibrium()
        self.solution(t)
        self.numerical_scope(t)
        self.working(t)
        self.data(t)
        self.puzzle(t)
        self.open_problems()
        self.question()
        self.worked_answer()

    def card(self):
        c = research_card(r"The competitive storage model", r"Can rational storers explain spikes, backwardation and the "
                          r"Working curve?", part=PART)
        with self.voiceover('For the researcher: the competitive storage model derives how constrained inventories can shape prices and forward spreads. We solve the original fixed numerical law on a bounded grid, not an exact continuous-state equilibrium. A separately pinned public price and inventory illustration follows, because legacy EIA workbook hashes no longer match. It describes association, not a calibrated model or causal test. We will derive the storage inequality, check numerical residuals and interpolation boundaries, distinguish price levels from log-price persistence, and identify questions the one-state model leaves open.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def equilibrium(self):
        rows = [cmath(r"x_t", r"=", r"I_{t-1} + z_t,\qquad p_t = P(x_t - I_t)", font_size=32, colors={r"x_t": INV}),
                cmath(r"P(x_t - I_t) + k", r"\ge", r"\beta\,\mathbb E_t\big[p_{t+1}\big],\ \ \text{with equality if } I_t > 0",
                      font_size=30, colors={r"P(x_t - I_t) + k": PRICE}),
                cmath(r"f(x)", r"=", r"\max\Big\{P(x),\ \beta\,\mathbb E\big[f(I^*(x) + z')\big] - k\Big\}", font_size=30,
                      colors={r"f(x)": PRICE}),
                cmath('F_t - p_t', '\\le', 'k/\\beta+(\\beta^{-1}-1)p_t,\\qquad\\text{equality if }I_t>0', font_size=28, colors={'F_t - p_t': SPR})]
        whys = [why(r"availability is what was stored plus the new harvest (or production); what is not stored is consumed, "
                    r"and inverse demand $P$ sets the price"),
                why(r"competitive storers buy today, pay the cost $k$, and sell next period: in equilibrium the "
                    r"discounted expected price cannot exceed today's plus the cost, and equals it whenever anyone stores"),
                why(r"so the price is a function of availability alone, the fixed point of this equation (Gustafson 1958; "
                    r"Williams and Wright 1991; Deaton and Laroque 1992)"),
                why('with risk-neutral storers the future is the expected price: at full carry when stocks are positive, at zero stocks the no-storage inequality gives an upper bound, not necessarily a negative spread. Risk-neutral storers and deterministic discounting are model assumptions')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            "The model starts with availability: last period's stored inventory plus this period's harvest. <bookmark mark='a'/> Consumption is availability minus nonnegative inventory, and inverse demand sets the price. <bookmark mark='b'/> Storers pay the storage cost today, so today's price plus cost must be at least the discounted expected next price, with equality if inventory is positive. <bookmark mark='c'/> The fixed point couples this condition to demand and tomorrow's availability. It assumes risk-neutral storers and a constant discount factor, not an estimated physical-to-pricing measure change. <bookmark mark='d'/> If the forward equals the expected next price, positive stocks imply a spread of storage cost divided by beta plus interest times today's price. At zero stocks the spread is only bounded above by that quantity; it need not be negative. A stock-out is not synonymous with backwardation."
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

    def solution(self, t):
        m = t["model"]
        x = np.asarray(m["x"])
        f = np.asarray(m["f"])
        I = np.asarray(m["I"])
        g = axes([0.5, 3.0], [0, 3.4], x_length=7.8, y_length=4.2, xlabel=r"availability $x$ (mean harvest 1)",
                 ylabel=r"price $f(x)$, and inventory carried $I(x)$", xticks=[0.5, 1, 1.5, 2, 2.5, 3],
                 yticks=[0, 1, 2, 3], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        pd_ = curve(ax, x, x ** -2.0, GREY_B, stroke_width=2)
        pf = curve(ax, x, f, PRICE, stroke_width=3.5)
        iv = curve(ax, x, I, INV, stroke_width=3)
        kink = x[np.argmax(I > 1e-6)]
        kl = DashedLine(ax.c2p(kink, 0), ax.c2p(kink, 3.4), color=GREY_C, stroke_width=1.5)
        kt = label(r"storage begins", font_size=14, color=GREY_B).next_to(ax.c2p(kink, 3.4), DOWN, buff=0.08)
        leg = legend([(GREY_B, r"consume everything: $P(x)$"), (PRICE, r"equilibrium price $f(x)$"),
                      (INV, r"inventory carried $I(x)$")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        p = t["params"]
        side = wrapped_label(f"demand elasticity {p['elasticity']}, harvests with standard deviation {p['harvest_sd']}, interest 1\\% and storage cost {100 * p['k']:.1f}\\% of the reference price $P(1)=1$ per period; time iteration converged in {m['iterations'] + 1} updates on 400 grid points; clamped interpolation and finite quadrature", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Solve it by time iteration: guess a price function, compute what storers would carry, and repeat until "
            "nothing changes. <bookmark mark='a'/> Without storage, the price would simply be demand at whatever is "
            "available. <bookmark mark='b'/> With it, plenty is smoothed: storers buy when availability is high and "
            "the price is flattened. <bookmark mark='c'/> But below the kink, nobody stores, and the price follows the "
            "steep demand curve: storage can carry a surplus forward, never a shortage backward."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(pd_), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(pf), Create(iv), FadeIn(leg[1]), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(kl), FadeIn(kt))
        self.wait(0.4)
        self.clear_scene()

    def working(self, t):
        m = t["model"]
        I = np.asarray(m["I"])
        sp = 100 * np.asarray(m["spread"])
        o = np.argsort(I)
        g = axes([-0.05, 2.0], [-70, 4], x_length=7.8, y_length=4.2, xlabel=r"inventory carried $I$",
                 ylabel=r"one-period spread $(F - p)/p$, \%", xticks=[0, 0.5, 1.0, 1.5], yticks=[-60, -40, -20, 0],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(-0.05, 0), ax.c2p(2.0, 0), color=GREY_C, stroke_width=1.2)
        pos = I > 1e-6
        line = curve(ax, I[pos], sp[pos], SPR, stroke_width=3.5)
        stock = VGroup(*[Dot(ax.c2p(0, v), radius=0.04, color=BAD) for v in sp[~pos][::12]])
        stats = VGroup(MathTex(rf"\text{{stock-outs}}:\ {100 * m['stockout_share']:.0f}\%\ \text{{of periods}}", font_size=24),
                       MathTex(rf"\text{{price skewness}}:\ {m['price_skew']:.1f}", font_size=24),
                       MathTex(rf"\text{{price autocorrelation}}:\ {m['price_ac1']:.2f}", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        fit_right(stats)
        side = wrapped_label('red: the stock-out states, all at zero inventory, with spreads down to $-66\\%$; 199{,}000 retained periods after 1{,}000 burn-in observations from the original fixed simulation', 3.3, 14, GREY_A).next_to(stats, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Now plot the one-period spread against inventory, retaining the full range down to minus sixty-six percent. <bookmark mark='a'/> With positive stocks the exact model identity is interest plus storage divided by beta and by spot. Because storage cost is an absolute amount, that fractional spread varies with price; it is not perfectly flat. <bookmark mark='b'/> At zero inventory several availability states share the same horizontal coordinate, so the red points form a vertical set rather than a single-valued curve. <bookmark mark='c'/> The original fixed simulation generates two hundred thousand periods and discards one thousand. Its remaining sample exhibits stock-outs and positive price skewness. These are properties of this chosen numerical example, not universal consequences of every nonnegative inventory constraint."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(line), run_time=1.3)
            vo.wait_until("b")
            self.play(FadeIn(stock))
            vo.wait_until("c")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
        self.wait(0.4)
        self.clear_scene()

    def data(self, t):
        d = t["data"]
        dev = 100 * np.asarray(d["dev"])
        sp = 100 * np.asarray(d["spread"])
        g = axes([-25, 45], [-12, 30], x_length=7.8, y_length=4.2, xlabel=r"US commercial crude stocks, \% above their "
                 r"5-year seasonal norm", ylabel=r"second WTI future over the first, \% (monthly average)",
                 xticks=[-20, 0, 20, 40], yticks=[-10, 0, 10, 20, 30], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(-25, 0), ax.c2p(45, 0), color=GREY_C, stroke_width=1.2)
        ok = np.isfinite(dev) & np.isfinite(sp)
        assert np.all((-25 <= dev[ok]) & (dev[ok] <= 45) & (-12 <= sp[ok]) & (sp[ok] <= 30))
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.03, color=OIL, fill_opacity=0.5) for a_, b_ in zip(dev[ok], sp[ok])])
        bins = d["bins"]
        bl = VGroup(curve(ax, [100 * b_["dev"] for b_ in bins], [100 * b_["spread"] for b_ in bins], WHITE, stroke_width=3.5),
                    *[Dot(ax.c2p(100 * b_["dev"], 100 * b_["spread"]), radius=0.07, color=WHITE) for b_ in bins])
        side = wrapped_label(rf"EIA: NYMEX WTI contracts 1 and 2, daily, and weekly stocks excluding the SPR; {d['n']} "
                             rf"months, 1990--2020; white: the means by decile of the inventory deviation; correlation "
                             rf"{d['corr']:.2f}; {100 * d['share_backwardation']:.0f}\% of months in backwardation", 3.3, 14,
                             GREY_A).to_edge(RIGHT, buff=0.3).shift(UP * 0.8)
        fit_right(side)
        lo, hi = bins[0], bins[-1]
        with self.voiceover(
            f"Here is a separately pinned public association for 1990 through 2020: the monthly average second-over-first WTI spread against US commercial crude stocks relative to a trailing seasonal norm. All observations are retained, including the large positive spread above twenty-six percent. <bookmark mark='a'/> Decile means rise from about {100 * lo['spread']:.1f} percent in the scarcest bin to {100 * hi['spread']:+.1f} in the most plentiful. Those spreads compare delivery contracts about a month apart; they are not realized monthly trading returns. <bookmark mark='b'/> April 2020 illustrates delivery and storage pressure, but these data do not measure each trader's accessible capacity or identify a causal inventory effect. The simple model has no upper storage-capacity constraint, and its positive-price law cannot represent negative oil."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(bl), run_time=1.3)
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self, t):
        m, a = t["model"], t["data_ac"]
        rows = [(r"model: price autocorrelation, one period", rf"{m['price_ac1']:.2f}"),
                (r"WTI: monthly log price autocorrelation, one month", rf"{a['monthly_log_price_ac1']:.2f}"),
                (r"WTI: twelve months", rf"{a['monthly_log_price_ac12']:.2f}")]
        tab = VGroup()
        for j, (a_, v) in enumerate(rows):
            r_ = VGroup(label(a_, font_size=20, color=GREY_A), MathTex(v, font_size=30, color=BAD if j else PRICE))
            r_[0].move_to([-1.6, 1.6 - 0.8 * j, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
            r_[1].move_to([5.0, 1.6 - 0.8 * j, 0])
            tab.add(r_)
        note_ = why(r"Deaton and Laroque (1992, 1996) found the same for thirteen commodities: the storage model gets "
                    r"the skewness and the spikes right and the persistence badly wrong. Cafiero, Bobenrieth, Bobenrieth "
                    r"and Wright (2011) argue a finer numerical solution and different demand narrow the gap; "
                    r"serially correlated supply and demand shocks close more of it").to_edge(DOWN, buff=0.5)
        if note_.width > 12.4:
            note_.scale_to_fit_width(12.4)
        with self.voiceover(
            f"The persistence comparison needs care. <bookmark mark='a'/> The saved model statistic is price-level autocorrelation, {m['price_ac1']:.2f} per abstract period. The public oil statistic is monthly log-price autocorrelation, {a['monthly_log_price_ac1']:.2f}, with twelve-month log-price correlation {a['monthly_log_price_ac12']:.2f}. These transformations and time units differ; they are not a like-for-like calibrated test. <bookmark mark='b'/> Deaton and Laroque's empirical work raised an important persistence puzzle for storage models. Later research showed that numerical accuracy, demand specification and persistent shocks can change the comparison. Our table motivates that literature without claiming the particular fixed example proves a universal inability of competitive storage to generate persistence."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Indicate(tab[0], scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: persistence", r"how much of commodity price persistence is storage and how much is "
                          r"persistent shocks to supply, demand or storage capacity is still argued", width=12.4,
                          font_size=18),
            desk_question(r"open: risk premia in the curve", r"with risk-averse storers and hedgers (Keynes's normal "
                          r"backwardation) the spread is no longer the expected price change; separating the two in data "
                          r"is unsettled", width=12.4, font_size=18),
            desk_question(r"open: capacity limits", r"storage tanks fill: an upper bound on inventory (April 2020) adds a "
                          r"second kink, and models with both bounds and financial traders are young", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> How much of commodity price persistence is storage, and how much "
            "is persistent shocks to supply, demand or storage capacity, is still argued. <bookmark mark='b'/> With "
            "risk-averse storers and hedgers, Keynes's normal backwardation, the spread is no longer the expected price "
            "change, and separating the two in data is unsettled. <bookmark mark='c'/> And tanks fill up: an upper bound "
            "on inventory, April 2020's lesson, adds a second kink, and models with both bounds and financial traders "
            "are young."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.15))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[k], scale_factor=1.01))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"spot oil is \$70, the one-month rate 0.4\%, and storage costs \$0.30 a barrel a month. What is the "
                       r"most the one-month future can trade above spot? Below it, how far can it go?")
        with self.voiceover(
            "Pause and predict. Spot oil at seventy dollars, a one-month rate of point four percent, and storage at "
            "thirty cents a barrel a month. What is the most the one-month future can trade above spot? And below it, "
            "how far can it go?"
        ):
            self.play(FadeIn(q))
        self.wait(3.0)
        self.clear_scene()

    def numerical_scope(self, t):
        m, params = t["model"], t["params"]
        x, f, inventory = (np.asarray(m[key]) for key in ("x", "f", "I"))
        z, weights = np.polynomial.hermite_e.hermegauss(15)
        weights /= weights.sum()
        next_state = inventory[:, None] + 1.0 + 0.1*z
        expected = np.sum(weights*np.interp(next_state, x, f), axis=1)
        residual = f + params["k"] - params["beta"]*expected
        positive = inventory > 1e-6
        euler = float(np.max(np.abs(residual[positive])))
        upper_mass = float(np.max(np.sum(weights*(next_state>x[-1]), axis=1)))
        cards = VGroup(
            desk_question(r"Finite numerical problem", r"400 grid points on $[0.55,3]$; 15 harvest quadrature nodes; 164 updates. This is not an exact continuous-state equilibrium.", width=12.0, font_size=20),
            desk_question(r"Residual check", rf"Maximum Euler residual for positive inventory: {euler:.2g}; stock-out inequality is nonnegative on the saved grid.", width=12.0, font_size=20),
            desk_question(r"Boundary check", rf"Worst grid-state quadrature mass clamped at the upper boundary: {100*upper_mass:.2f}\%. The original fixed-seed simulation stayed inside the grid; this does not control every possible state.", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover('The numerical certificate is deliberately limited. On four hundred grid points, the positive-stock Euler residual is below one billionth and the zero-stock inequality holds. But the expectation uses fifteen quadrature nodes with clamped interpolation. At the worst upper-boundary grid state, about one point nine percent of quadrature mass lies outside the grid and is clamped; a tiny lower-tail mass is clamped too. The original fixed-seed two-hundred-thousand-period simulation stayed within the grid. That observed path does not certify all possible states, quadrature accuracy or a global continuous equilibrium. Smaller residuals of a discretized equation do not by themselves establish small approximation error.'):
            self.play(LaggedStart(*[FadeIn(card) for card in cards],lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def worked_answer(self):
        rows = VGroup(
            label(r"Accessible storage, known rate, cost paid today", font_size=28),
            MathTex(r"F \le (70+0.30)(1.004)=70.5812",font_size=38,color=SPR),
            MathTex(r"F-70 \le 0.5812",font_size=36),
            wrapped_label(r"If storage is paid at delivery the bound is 0.58. One-way cash and carry supplies no analogous lower carry bound; the positive-price storage model does not describe negative oil.",12.0,21,GREY_A),
        ).arrange(DOWN,buff=0.4)
        with self.voiceover('With storage accessible at thirty cents paid today, finance both the seventy-dollar barrel and storage for one month. The locked delivery cost is seventy point three times one point zero zero four, or seventy point five eight one two dollars. Thus the upper spread bound is about fifty-eight cents. If storage is paid at delivery instead, it is exactly fifty-eight cents under these inputs. One-way cash and carry does not provide an analogous lower carry bound without the reverse trade. That statement does not say every price model permits arbitrarily negative futures: our positive-price storage law cannot represent negative oil, while an actual contract may permit it.'):
            self.play(FadeIn(rows))
        self.wait(0.5)
        self.clear_scene()
