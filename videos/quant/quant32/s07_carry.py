from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, PART, CARRY_C, fit_right
from videos.quant.quant32.illustrations import currency_case


class Carry(VoiceoverScene):
    def construct(self):
        self.card()
        self.deposit(currency_case())
        self.forward(currency_case())
        self.currency_risk(currency_case())
        self.curve()
        self.payoffs()
        self.residual()
        self.oil()
        self.bonds()
        self.premia()
        self.question()

    def card(self):
        c = chapter_card(6, r"Carry, made visible", r"What is observable now, and what remains a risky future price?",
                         part=PART)
        with self.voiceover(
            "Chapter six. Carry describes return components under a specified convention about prices "
            "and financing. Rates, forward prices and a curve can be observed now. The later spot "
            "price is still uncertain. We will use fixed currency and commodity examples to separate "
            "those quantities, rather than treating a fund-minus-spot residual as an identified premium."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def deposit(self, a):
        rows = VGroup(
            MathTex(r"1+R_{\rm foreign\ deposit}^{\rm domestic}=(1+r_f)\frac{S_T}{S_0}", font_size=35),
            MathTex(r"R_{\rm excess}=(1+r_f)(1+s)-1-r_d", font_size=36),
            MathTex(r"r_f=6\%,\quad r_d=2\%,\quad s=0:\quad R_{\rm excess}=4\%", font_size=32),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen one-year simple deposit rates; S is domestic currency per foreign unit; "
                             r"no fees, credit losses or transaction costs", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Start with deposits and quote the exchange rate as domestic currency per foreign unit. "
            "One domestic dollar buys one over the initial spot rate in foreign units. After earning "
            "the foreign deposit rate, those units are converted at the terminal spot rate. "
            "<bookmark mark='a'/> The domestic gross return is one plus the foreign rate times one "
            "plus the spot change. Subtract the domestic cash return to define the excess return. "
            "<bookmark mark='b'/> Choose simple annual rates six and two percent and an unchanged "
            "spot rate. Excess return is four percent. The calculation assumes the rates are "
            "available on the stated terms, with no credit loss, fees or trading costs."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def forward(self, a):
        rows = VGroup(
            MathTex(r"F_0=S_0\frac{1+r_d}{1+r_f}", font_size=40),
            MathTex(rf"S_0={a['spot']:.2f},\quad r_f=6\%,\quad r_d=2\%:\quad F_0={a['forward']:.5f}",
                    font_size=33),
            MathTex(r"\text{long forward on one foreign unit: PnL}=S_T-F_0", font_size=33),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen frictionless one-year covered-interest-parity convention; matched credit "
                             r"and funding terms; forward PnL is in domestic currency, not a capital return",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Covered interest parity links the forward quote to the two funding rates under matched "
            "credit and frictionless borrowing and lending assumptions. "
            f"<bookmark mark='a'/> With initial spot {a['spot']:.2f} and our six-versus-two-percent "
            f"rates, the one-year forward is {a['forward']:.5f} domestic units per foreign unit. "
            "The higher-yielding foreign currency has a forward discount under this quote convention. "
            "<bookmark mark='b'/> A long forward on one foreign unit earns terminal spot minus the "
            "contracted forward, in domestic currency. It starts without paying that full notional, "
            "so a percentage return also needs a capital and collateral convention. Covered parity "
            "does not determine expected terminal spot or guarantee a profitable unhedged carry trade."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def currency_risk(self, a):
        head = label(r"Chosen spot changes, same deposit rates", font_size=30).to_edge(UP, buff=0.5)
        rows = VGroup(*[
            label(rf"spot {100 * x['spot_change']:+.0f}\%: foreign-deposit total "
                  rf"{100 * x['foreign_deposit_total']:+.1f}\%, excess {100 * x['excess_over_domestic']:+.1f}\%",
                  font_size=25, color=BAD if x["excess_over_domestic"] < 0 else CARRY_C)
            for x in a["cases"]
        ]).arrange(DOWN, buff=0.6)
        equation = MathTex(r"R_{\rm excess}=r_f-r_d+s+r_fs", font_size=37).shift(DOWN * 2.0)
        foot = wrapped_label(r"stipulated one-year terminal spots, not a sample or currency ranking",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(head), FadeIn(rows[1]), FadeIn(foot))
        with self.voiceover(
            "An observable rate difference leaves exchange-rate risk. Keep the same six and two "
            "percent deposit rates. If spot is unchanged, the foreign deposit earns six percent "
            "in domestic units, or four percent above domestic cash. "
            "<bookmark mark='a'/> Choose a five percent fall in the foreign currency instead. Its "
            "domestic total return is point seven percent, and excess return is minus one point "
            "three percent. A five percent rise gives eleven point three percent total and nine "
            "point three percent excess. "
            "<bookmark mark='b'/> Expanding the product shows the rate difference, the spot change "
            "and their cross term. Dropping that term is an approximation. A large quoted carry "
            "does not control the price change that can outweigh it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(Write(equation))
        self.clear_scene()

    def curve(self):
        maturity = np.linspace(0, 2, 121)
        g = axes([0, 2], [89, 112], x_length=8.1, y_length=4.2,
                 xlabel=r"chosen maturity, years", ylabel=r"forward price, domestic units",
                 xticks=[0, 1, 2], yticks=[90, 100, 110], font_size=16).move_to(LEFT * 1.4)
        up = curve(g.ax, maturity, 100 * np.exp(0.05 * maturity), BAD, stroke_width=3)
        down = curve(g.ax, maturity, 100 * np.exp(-0.05 * maturity), GOOD, stroke_width=3)
        leg = legend([(BAD, r"chosen contango"), (GOOD, r"chosen backwardation")],
                     font_size=17).to_edge(RIGHT, buff=0.35).shift(UP * 1.2)
        fit_right(leg)
        foot = wrapped_label(r"chosen spot 100 and continuous net carry +5\% or -5\%; stylised storage-pricing "
                             r"reference, no observed commodity series", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(g), Create(up), FadeIn(leg), FadeIn(foot))
        with self.voiceover(
            "For a storable commodity, a stylised storage-pricing reference writes a forward as spot "
            "times the exponential of financing plus storage cost minus convenience yield. "
            "<bookmark mark='a'/> Choose spot one hundred and net carry plus five percent or minus "
            "five percent in continuous annual units. The upward curve is contango and the downward "
            "curve backwardation. "
            "<bookmark mark='b'/> The pricing argument needs the ability to carry the commodity and "
            "the relevant funding, storage and trading assumptions. Convenience benefits and physical "
            "constraints matter. Neither curve alone specifies expected terminal spot. In particular, "
            "a forward premium over today's spot is not proof of a negative expected futures profit."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(down))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def payoffs(self):
        rows = VGroup(
            MathTex(r"F_0=105,\quad S_T=100:\quad P=-5", font_size=36),
            MathTex(r"F_0=105,\quad S_T=120:\quad P=+15", font_size=36),
            MathTex(r"F_0=95,\quad S_T=90:\quad P=-5", font_size=36),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"separate chosen long-contract examples, one commodity unit, domestic-currency PnL; "
                             r"no margin or percentage capital-return convention", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Three fixed contract payoffs make the distinction explicit. A long contract entered at "
            "one hundred five and settled at one hundred loses five currency units. "
            "<bookmark mark='a'/> The same entry price settled at one hundred twenty gains fifteen. "
            "A contract initially above spot can therefore make money when terminal spot rises enough. "
            "<bookmark mark='b'/> Conversely, entry at ninety-five followed by settlement at ninety "
            "loses five, even if ninety-five was initially below spot. Convergence is a relation "
            "between futures and spot at delivery, not a promise that today's spot stays fixed. "
            "Rolling changes contracts; its realised contribution also needs the intervening curve "
            "and financing path, rather than subtracting today's quoted gap every month."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def residual(self):
        cards = VGroup(
            desk_question(r"exact deposit arithmetic", r"rate difference, spot change and cross term have "
                          r"explicit units and cash-flow assumptions", width=12.2, font_size=20),
            desk_question(r"fund-minus-spot residual", r"fees, collateral, distributions, tracking, rolls and "
                          r"benchmark conventions can all enter", width=12.2, font_size=20),
            desk_question(r"measurement", r"compounding daily excess returns and adding a monthly cash rate "
                          r"does not generally recover exact compounded total returns", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "A deposit identity is not automatically a fund attribution. A currency or commodity "
            "fund has expenses, collateral policies, distributions and tracking conventions. "
            "<bookmark mark='a'/> Its realised return minus a chosen spot benchmark can contain "
            "all of these effects, as well as different price clocks and contract exposures. Calling "
            "the whole residual an identified interest differential or pure roll yield is too strong. "
            "<bookmark mark='b'/> Compounding daily excess returns also differs from compounding "
            "total returns and then subtracting compounded cash. Adding a monthly cash return "
            "does not generally undo the cross terms. State the construction before comparing "
            "numbers, and distinguish an observable forward carry measure from a realised residual."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def oil(self):
        c = crisis_card(r"20 April 2020", r"The expiring May WTI contract",
                        r"The reported settlement was -37.63 dollars per barrel. Contract delivery and storage "
                        r"constraints matter; this quotation is not a negative spot series or a fund return.",
                        width=11.8, font_size=22)
        source = note(r"CME WTI settlement reporting, 20 April 2020", font_size=18,
                      color=GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(c), FadeIn(source))
        with self.voiceover(
            "The crisis file is a specific contract, not a generic oil price. The expiring May "
            "West Texas Intermediate contract settled at minus thirty-seven dollars and sixty-three "
            "cents per barrel on April twentieth, 2020, as reported. Delivery and storage constraints "
            "near expiry were central to that episode. A fund can hold other maturities and change "
            "its roll policy. Its return cannot be inferred from this settlement quotation alone. "
            "The quotation also does not supply an observed negative spot-price path for our "
            "chosen mathematical curves."
        ):
            self.wait(0.2)
        self.clear_scene()

    def bonds(self):
        rows = VGroup(
            MathTex(r"\text{carry/roll approximation}\approx y-r_{\rm cash}-D\,\Delta y_{\rm roll}", font_size=31),
            MathTex(r"y=3\%,\ r_{\rm cash}=2\%,\ D=5,\ \Delta y_{\rm roll}=-0.001:\quad 1.5\%", font_size=29),
            MathTex(r"\text{additional yield rise }0.01:\quad 1.5\%-5(0.01)=-3.5\%", font_size=31),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen one-year first-order example under a specified curve-roll assumption; "
                             r"no convexity, coupon reinvestment, other fees or empirical bond return",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Bonds have financing and roll components too. Under a stated local approximation, "
            "yield over the cash rate and the price effect of rolling to another point on a fixed "
            "curve contribute to carry. Curve slope alone is not the entire return. "
            "<bookmark mark='a'/> Choose yield three percent, cash two percent, duration five, "
            "and an assumed roll-related yield decline of one tenth of a percentage point over "
            "the year. The approximation gives one point five percent. "
            "<bookmark mark='b'/> An additional one-percentage-point yield rise subtracts about "
            "five percent, producing minus three point five percent. These fixed assumptions "
            "omit convexity and other cash flows. Observable carry can coexist with substantial price risk."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def premia(self):
        cards = VGroup(
            desk_question(r"hedging demand", r"Keynes-Hicks style theories can relate risk premia to hedgers' "
                          r"demand; curve shape alone does not identify the premium", width=12.2, font_size=20),
            desk_question(r"common losses", r"currency, funding and liquidity shocks can affect high-carry "
                          r"positions together; the mechanism and evidence must be distinguished",
                          width=12.2, font_size=20),
            desk_question(r"research design", r"an ex-ante ranking needs available rates or curve inputs, fixed "
                          r"units, costs and an independent evaluation", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Why might a carry premium exist? Hedging-demand theories associated with Keynes and "
            "Hicks propose compensation for bearing risks that others want to transfer. The "
            "expected spot-versus-forward gap is still an economic hypothesis, not an implication "
            "of today's curve slope. "
            "<bookmark mark='a'/> Funding and liquidity shocks can create common losses among "
            "leveraged carry positions. That is a possible mechanism; identifying its role in a "
            "particular episode needs more than a negative sample skew. "
            "<bookmark mark='b'/> A testable carry rule therefore specifies its ex-ante inputs, "
            "quote conventions, ranking, collateral, costs and evaluation period. A realised "
            "fund residual and a forward carry measure should not be silently interchanged."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('r_f=6\\%,\\quad r_d=2\\%,\\quad s=-5\\%', font_size=34),
            MathTex('R_{\\rm total}=(1+r_f)(1+s)-1', font_size=34),
            MathTex('R_{\\rm excess}=R_{\\rm total}-r_d', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Foreign deposit 6\%, domestic cash 2\%, foreign currency spot change -5\% over one year. "
                       r"What are the domestic total and excess returns, before fees?")
        with self.voiceover(
            "Pause and predict. A foreign deposit pays six percent, domestic cash pays two "
            "percent, and the foreign currency falls five percent over the year. What are "
            "the domestic-currency total return and excess return? Retain the cross term, "
            "and distinguish the answer from a forward's profit per foreign unit."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
