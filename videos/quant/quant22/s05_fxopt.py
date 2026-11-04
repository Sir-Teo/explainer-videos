from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class FXOptions(VoiceoverScene):
    def construct(self):
        x = load("fxopt")
        self.card()
        self.derive()
        self.symmetry()
        self.price(x)
        self.deltas(x)
        self.premium(x)
        self.atm(x)

    def card(self):
        c = chapter_card(4, r"FX options: two rates and four deltas", r"How is a currency option quoted and hedged?",
                         lit=(), part=PART)
        with self.voiceover("Chapter four. Currency options: one formula, two interest rates, and four ways to say "
                            "delta."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"dS", r"=", r"(r_d - r_f)\,S\,dt + \sigma S\,dW^{\mathbb{Q}}", font_size=40, colors={r"dS": FOR}),
                cmath(r"C", r"=", r"S e^{-r_f T} N(d_1) - K e^{-r_d T} N(d_2),\quad d_{1,2} = \frac{\ln(F/K) \pm "
                      r"\tfrac12\sigma^2 T}{\sigma\sqrt T}", font_size=32, colors={r"C": USD}),
                cmath(r"C - P", r"=", r"S e^{-r_f T} - K e^{-r_d T} = e^{-r_d T}(F - K)", font_size=36)]
        whys = [why(r"a unit of foreign currency is an asset that pays interest at $r_f$: in the domestic risk-neutral "
                    r"world it drifts at $r_d - r_f$, exactly like a stock with dividend yield $r_f$"),
                why(r"Garman and Kohlhagen (1983): Black--Scholes with the foreign rate as the dividend. $S$ and $K$ in "
                    r"domestic per foreign; the price is in domestic currency per unit of foreign notional"),
                why(r"put--call parity is covered interest parity again: the forward $F = S e^{(r_d - r_f)T}$ of chapter 1")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "A unit of foreign currency is an asset that pays interest: hold a euro and it earns the euro rate. So, "
            "seen from dollars, its risk-neutral drift is the dollar rate less the euro rate, exactly like a stock with "
            "a dividend yield. <bookmark mark='a'/> In 1983 Mark Garman and Steven Kohlhagen wrote down what follows: "
            "the Black-Scholes formula, with the foreign rate in place of the dividend. <bookmark mark='b'/> And "
            "put-call parity becomes covered interest parity: a call less a put is a forward, struck at the parity "
            "forward of chapter one."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def symmetry(self):
        rows = [cmath(r"C_{\text{EUR}/\text{USD}}(S, K)", r"=", r"S\,K\;P_{\text{USD}/\text{EUR}}\big(\tfrac1S, \tfrac1K\big)",
                      font_size=36, colors={r"C_{\text{EUR}/\text{USD}}(S, K)": USD})]
        whys = [why(r"every currency option is a call on one currency and a put on the other: the right to buy euros "
                    r"for dollars at $K$ is the right to sell $K$ dollars for one euro. Priced in dollars per euro on "
                    r"one side, in euros per dollar on the other; the factor $S K$ converts units and notional")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.4, buff=0.8, edge=6.9)
        cards = VGroup(
            desk_question(r"quoted how?", r"in domestic pips (dollars per euro of notional), or as a percentage of "
                          r"either notional; the market agrees which by currency pair", width=12.0, font_size=20),
            desk_question(r"which way round?", r"a euro call is a dollar put: two desks, in two countries, can hold the "
                          r"same contract and call it by opposite names", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Currency options have a symmetry stocks do not. The right to buy a euro for K dollars is the right to sell "
            "K dollars for one euro: a euro call is a dollar put. <bookmark mark='a'/> Price it from either side and "
            "the formulas agree, once the units and the notional are converted. <bookmark mark='b'/> So the market "
            "has conventions for everything: which currency the price is in, which notional it is a percentage of, "
            "and which way round the option is named. Two desks in two countries can hold the same contract and call "
            "it by opposite names."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def price(self, x):
        q = x["quotes"]
        rows = VGroup(
            label(r"An illustrative EUR/USD market, three months", font_size=24, color=GREY_A),
            MathTex(rf"S = {x['S']:.4f},\ r_\$ = {100 * x['rd']:.1f}\%,\ r_\text{{\texteuro}} = {100 * x['rf']:.1f}\%,\ "
                    rf"F = {x['F']:.4f}", font_size=32),
            MathTex(rf"\sigma_{{\text{{ATM}}}} = {100 * q['atm']:.1f}\%:\quad C = {x['gk_atm']:.4f}\ \$\ \text{{per}}\ "
                    rf"\text{{\texteuro}} = {x['gk_pips']:.0f}\ \text{{pips}}", font_size=32, color=USD),
            MathTex(rf"\text{{on \texteuro}}10\text{{m}}:\ \${1e7 * x['gk_atm']:,.0f};\ \text{{vega}}\ \${1e7 * x['vega_atm']:,.0f}"
                    rf"\ \text{{per vol point}}".replace(",", "{,}"), font_size=30),
            wrapped_label(r"pips: units of 0.0001 dollars per euro. Illustrative inputs, close to the market of 2025, not "
                          r"a record of any day", 12.0, 17, GREY_A),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Put numbers in. A euro at one dollar ten, three-month dollar rates at four point three percent and euro "
            "rates at two, so the forward is above spot, as parity requires. <bookmark mark='a'/> At seven and a half "
            f"percent volatility the at-the-money call is worth about {x['gk_pips']:.0f} pips: "
            f"{x['gk_pips']:.0f} ten-thousandths of a dollar per euro, or about {1e7 * x['gk_atm'] / 1000:.0f} thousand "
            f"dollars on ten million euros, and each point of volatility moves it by {1e7 * x['vega_atm'] / 1000:.0f} "
            "thousand. Currency options are quoted and traded as volatility; the formula only converts."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()

    def deltas(self, x):
        d = x["deltas"]
        rows = [(r"spot delta", r"e^{-r_f T} N(d_1)", "spot"), (r"forward delta", r"N(d_1)", "forward"),
                (r"spot, premium-adjusted", r"e^{-r_f T}\tfrac{K}{F} N(d_2)", "spot_pa"),
                (r"forward, premium-adjusted", r"\tfrac{K}{F} N(d_2)", "forward_pa")]
        hx = [-3.9, 0.3, 3.9]
        tab = VGroup(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x_, 2.2, 0]) for h_, x_ in
                              zip([r"convention", r"formula", r"the 25-delta call"], hx)]))
        for i, (nm, fm, k) in enumerate(rows):
            y = 1.5 - 0.7 * i
            tab.add(VGroup(label(nm, font_size=20).move_to([hx[0], y, 0]), MathTex(fm, font_size=30).move_to([hx[1], y, 0]),
                           MathTex(f"{d[k]:.4f}", font_size=30, color=BASIS if k.endswith("pa") else USD).move_to(
                               [hx[2], y, 0])))
        foot = wrapped_label(r"the same option, the strike the market calls 25-delta under the forward convention. Spot "
                             r"delta hedges with spot; forward delta with a forward; premium adjustment subtracts the "
                             r"premium when it is paid in the foreign currency, since that premium is itself a position "
                             r"in the currency", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now delta. In stocks it is one number. In currencies there are four, and the market uses all of them. "
            "<bookmark mark='a'/> Spot delta is the hedge in spot currency. Forward delta is the hedge in the forward, "
            "without the discount factor. <bookmark mark='b'/> And when the premium is paid in the foreign currency, "
            "as it is for the dollar against the yen, the premium itself is a position in that currency, and the "
            "hedge must net it out: the premium-adjusted deltas. For the same option they differ in the third "
            "decimal, which on a billion of notional is a few million dollars of hedge."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def premium(self, x):
        p = x["pa"]
        kk, dpa, dnp = np.asarray(p["kk"]), np.asarray(p["dpa"]), np.asarray(p["dnp"])
        g = axes([kk[0], kk[-1]], [0, 1.0], x_length=7.4, y_length=4.2, xlabel=r"strike, yen per dollar",
                 ylabel=r"call delta", xticks=[100, 150, 200, 250], yticks=[0, 0.25, 0.5, 0.75, 1.0], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        l1 = curve(ax, kk, dnp, USD, stroke_width=3)
        l2 = curve(ax, kk, dpa, BASIS, stroke_width=3)
        pk = int(np.argmax(dpa))
        dot = Dot(ax.c2p(kk[pk], dpa[pk]), color=BASIS)
        side = VGroup(
            legend([(USD, r"forward delta"), (BASIS, r"forward, premium-adjusted")], font_size=17),
            MathTex(rf"\max\Delta_{{pa}} = {dpa[pk]:.2f}\ \text{{at}}\ K = {kk[pk]:.0f}", font_size=24, color=BASIS),
            wrapped_label(r"an illustrative dollar-yen market: spot 150, dollar rate 4.3\%, yen 0.5\%, volatility 10\%, "
                          r"three months. Below the peak, two strikes share each premium-adjusted delta: a desk asking "
                          r"for 'the 25-delta call' must say which side", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Premium adjustment has a strange consequence. <bookmark mark='a'/> The ordinary call delta falls from one "
            "to zero as the strike rises. <bookmark mark='b'/> The premium-adjusted delta does not: deep in the money, "
            "the premium is almost the whole option, so subtracting it pulls the delta back down. It rises, peaks "
            f"below one, at about {dpa[pk]:.2f}, and falls. So a premium-adjusted delta can name two strikes, and the "
            "market's convention is to take the one above the peak."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(dot), FadeIn(side[1]), FadeIn(side[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def atm(self, x):
        rows = [cmath(r"K_{\text{ATMF}}", r"=", r"F", font_size=40),
                cmath(r"K_{\text{DNS}}", r"=", r"F\,e^{\frac12\sigma^2 T}\quad\big(F\,e^{-\frac12\sigma^2 T}\ \text{premium-"
                      r"adjusted}\big)", font_size=36, colors={r"K_{\text{DNS}}": BASIS})]
        whys = [why(r"'at the money' could mean the spot, the forward, or the strike where a call and a put have "
                    r"equal and opposite delta: the delta-neutral straddle, the market's standard"),
                why(rf"here $F$ = {x['F']:.4f} and $K_\text{{DNS}}$ = {x['K']['atm']:.4f}: a straddle there has no delta "
                    r"to hedge, so it trades as pure volatility. Every vol quote in the next chapter is pinned to it")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Even at-the-money has conventions. It could mean the spot, or the forward. <bookmark mark='a'/> The market "
            "means neither: it means the strike where a straddle, a call plus a put, has no delta at all, so that the "
            "straddle is a pure bet on volatility. That strike sits a little above the forward, by half the variance. "
            f"Here, {x['K']['atm']:.4f} against a forward of {x['F']:.4f}. Every volatility quote in the next chapter "
            "is anchored to it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"you are long a dollar-yen call and your hedge ratio comes from spot delta, but the premium was paid in "
                r"dollars. Are you over- or under-hedged, and by roughly how much?")
        with self.voiceover("You are long a dollar-yen call, hedged with spot delta, but the premium was paid in dollars. "
                            "Are you over- or under-hedged, and by roughly how much?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
