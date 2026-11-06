from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, Q_C, answer_under, illustration, load,
                                        pause_at)


class Industry(VoiceoverScene):
    def construct(self):
        sv, fb = load("sv_sim"), load("futures_basis")
        self.card()
        self.etfs()
        self.boxes(fb)
        self.convergence()
        self.limits(sv)
        self.ltcm()
        self.predict()

    def card(self):
        c = chapter_card(17, r"How arbitrage is traded, and why it is limited", r"Who keeps prices in line, and what "
                         r"stops them?", lit=(1998,), part=PART)
        with self.voiceover("Chapter seventeen. How arbitrage is traded, and why it is limited."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def etfs(self):
        f = firm_card(r"Authorized participants (ETF arbitrage)",
                      r"Large dealers that may create ETF shares by delivering the basket of underlying securities to "
                      r"the fund, or redeem shares for the basket. When an ETF trades above the value of its holdings "
                      r"(its NAV), they buy the basket, create shares and sell them; below, they buy shares and redeem. "
                      r"The SEC's Rule 6c-11 (2019) standardized how most ETFs work.",
                      source=r"SEC, Rule 6c-11 adopting release (2019)", width=6.6, font_size=21)
        c = crisis_card(r"March 2020", r"Bond ETFs below their holdings",
                        r"In the dash for cash, the most liquid bond ETFs traded at large discounts to their NAV, larger "
                        r"for Treasury, municipal and investment-grade funds than for high-yield ones: investors sold "
                        r"what was easiest to sell, and dealers' balance sheets, the arbitrage's capital, were full. "
                        r"The discounts closed almost as fast as they opened once the Fed stepped in.",
                        width=6.0, font_size=21)
        VGroup(f, c).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.1)
        src = note(r"Haddad, Moreira and Muir (2021), ``When selling becomes viral'', \textit{RFS} 34(11)", font_size=17,
                   color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Who enforces the law of one price? An ETF's shares and its holdings both trade all day. Authorized participants, large dealers, create shares by delivering the basket when the fund is dear, and redeem them when it is cheap; the SEC standardized this in 2019. <bookmark mark='a'/> It works until the arbitrageurs' capital is the constraint. In March 2020 the most liquid bond funds traded at large discounts to their holdings, larger for safer bonds, as Haddad, Moreira and Muir documented: investors sold what was easiest to sell, and dealers' balance sheets were full. A worked example: if a fund trades one percent above its basket, an authorized participant buys the basket, delivers it for new shares and sells them, earning the one percent less its costs, and the selling pushes the price back. Bond ETF holdings may have stale or estimated marks, creation baskets can differ from published holdings, and costs and balance-sheet constraints matter. A reported discount to NAV is not automatically an executable arbitrage."
        ) as vo:
            self.play(FadeIn(f, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c, shift=UP * 0.2), FadeIn(src))
        self.wait(0.3)
        self.clear_scene()

    def boxes(self, fb):
        cards = VGroup(
            history_card(r"1996--2023", r"van Binsbergen, Diamond and Van Tassel (New York Fed)", r"box-spread rates "
                         r"on S\&P 500 options sat 35 basis points above Treasury yields on average, January 1996 to "
                         r"April 2023", width=4.3, font_size=18),
            history_card(r"2022", r"van Binsbergen, Diamond and Grotteria, \textit{JFE}", r"risk-free rates read from "
                         r"put--call parity: Treasuries' convenience yield is about 40 basis points, larger below three "
                         r"months, and it quadrupled in the financial crisis", width=4.3, font_size=18),
            firm_card(r"BOXX", r"an ETF holding S\&P 500 box spreads: a loan to the options market, packaged",
                      numbers=[(r"\$8.08\text{bn}", r"net assets, 30 Sept.\ 2025"), (r"2022", r"inception, 27 December")],
                      source=r"Alpha Architect 1--3 Month Box ETF, annual report (SEC Form N-CSR)", width=4.3,
                      font_size=18),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).to_edge(UP, buff=0.5)
        foot = wrapped_label(rf"the crypto version, chapter 1: on {fb['n_matched']} Deribit expiries the options' "
                             rf"forward and the futures agreed to {fb['gap_p50']:.1f} basis points: the cash-and-carry "
                             rf"desks had already done their work", 11.6, 21, Q_C).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"The box spread as a business. At the New York Fed, van Binsbergen, Diamond and Van Tassel found box rates thirty-five basis points above Treasuries on average, 1996 to 2023. <bookmark mark='a'/> The gap is Treasuries' convenience yield, about forty basis points by van Binsbergen, Diamond and Grotteria, and it quadrupled in the financial crisis. <bookmark mark='b'/> A fund now lends through boxes: BOXX, launched at the end of 2022, held eight billion dollars by September 2025, its annual report says. <bookmark mark='c'/> And chapter one's crypto version agreed to {fb['gap_p50']:.1f} basis points. The thirty-five-basis-point estimate is a specific 1996-to-April-2023 sample; the roughly forty-point figure is a separate study, not an identical estimate. Collateral, taxes, settlement and trading costs differ. Our crypto comparison uses asynchronous observations."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def convergence(self):
        cards = VGroup(
            history_card(r"1980--1995", r"Royal Dutch and Shell", r"one company's profits split 60:40 between two "
                         r"listed shares; their prices deviated from the 60:40 ratio by 9.53\% on average (Froot and "
                         r"Dabora 1999; the RBA's replication)", width=4.3, font_size=18),
            history_card(r"1985--2000", r"Negative stubs", r"82 cases of a parent worth less than its stake in a listed "
                         r"subsidiary; in 30\% the link was severed before the gap closed (Mitchell, Pulvino and "
                         r"Stafford 2002)", width=4.3, font_size=18),
            history_card(r"2004", r"Ofek, Richardson and Whitelaw", r"parity violations concentrated where shorting was "
                         r"costly or constrained, and predicted the stocks' later underperformance", width=4.3,
                         font_size=18),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.4)
        with self.voiceover(
            """Convergence trades with funding and event risk. Royal Dutch and Shell's economic split was sixty to forty, yet the reported mean absolute deviation from parity was about nine and a half percent over 1980 to 1995. <bookmark mark='a'/> Negative-stub trades face an additional hazard: Mitchell, Pulvino and Stafford report that the relevant link was severed before convergence in about thirty percent of their sample. <bookmark mark='b'/> Borrow availability, recall, capital and event risk can prevent a theoretically attractive price relation from being a riskless executable trade."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def limits(self, sv):
        ex = sv["examples"]["1.0"]
        T = sv["T"]
        d_lo = min(-0.02, min(min(e["D"]) for e in ex) * 1.1)
        d_hi = max(0.09, max(max(e["D"]) for e in ex) * 1.1)
        c_lo = min(0.0, min(min(e["cap"]) for e in ex) * 1.1)
        c_hi = max(1.6, max(max(e["cap"]) for e in ex) * 1.1)
        g1 = axes([0, T], [d_lo, d_hi], x_length=5.6, y_length=2.4, ylabel=r"the mispricing $D_t$",
                  xticks=[], yticks=[0, 0.04, 0.08], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15)
        g2 = axes([0, T], [c_lo, c_hi], x_length=5.6, y_length=2.4, ylabel=r"the fund's capital", xlabel=r"period",
                  xticks=[0, 10, 20], yticks=np.linspace(c_lo, c_hi, 5).round(2).tolist(), font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        fl = DashedLine(g2.ax.c2p(0, sv["floor"]), g2.ax.c2p(T, sv["floor"]), color=ARB, stroke_width=2)
        fll = label(r"margin floor", font_size=16, color=ARB).next_to(g2.ax.c2p(T, sv["floor"]), UP, buff=0.05).shift(LEFT * 0.6)
        cols = [FWD, CALL, ALT]
        k = ValueTracker(0)

        def paths():
            v = k.get_value()
            out = VGroup()
            for e, c in zip(ex, cols):
                D, cap = np.asarray(e["D"]), np.asarray(e["cap"])
                n = min(len(D), int(v) + 1)
                if n >= 2:
                    out.add(curve(g1.ax, np.arange(n), D[:n], c, stroke_width=3),
                            curve(g2.ax, np.arange(n), cap[:n], c, stroke_width=3))
                if e["dead"] and v >= len(D) - 1:
                    out.add(Cross(scale_factor=0.12, stroke_color=ARB).move_to(g2.ax.c2p(len(cap) - 1, cap[-1])))
            return out

        Pth = always_redraw(paths)
        rows = sv["rows"]
        tab = VGroup(*[MathTex(rf"a = {r_['a']:.1f}:\ \ {100 * r_['p_liq']:.1f}\%", font_size=28,
                               color=ARB if r_['p_liq'] > 0 else CALL) for r_ in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.15)
        r1 = [r_ for r_ in rows if r_["a"] == 1.0][0]
        side = VGroup(
            wrapped_label(r"Shleifer and Vishny (1997): arbitrageurs manage other people's money, and investors "
                          r"withdraw $a$ times any loss", 4.6, 20, GREY_A),
            label(r"forced liquidations before convergence, 1{,}000 paths each:", font_size=19, color=GREY_A),
            tab,
            wrapped_label(rf"with $a = 1$, the fund is liquidated with the mispricing at {100 * r1['d_at_liq']:.1f}\% on "
                          rf"average, wider than the typical path's worst, {100 * r1['d_max_mean']:.1f}\%: it is forced "
                          rf"out when the trade is best", 4.6, 19, ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        src = illustration(r"simulated: the mispricing is a Brownian bridge to zero; leverage 6; seeded")
        verdict = ("without flows, none are liquidated. " if rows[0]["p_liq"] == 0 else
                   f"even without flows, {100 * rows[0]['p_liq']:.1f} percent are liquidated. ")
        with self.voiceover(
            f"Shleifer and Vishny, The Limits of Arbitrage, 1997: arbitrageurs invest other people's money, judged on recent returns. Simulate it: a mispricing certain to close by period twenty, a levered fund, and investors who pull a times any loss. <bookmark mark='a'/> When the mispricing widens, capital is withdrawn, and at the margin floor the fund is liquidated, missing the convergence it was right about. <bookmark mark='b'/> A thousand paths each: {verdict}With flows equal to the loss, {100 * r1['p_liq']:.1f} percent; twice the loss, {100 * rows[-1]['p_liq']:.1f}. <bookmark mark='c'/> And liquidations come when the mispricing is widest: arbitrage is limited by funding, not insight. Convergence by period twenty is imposed by this stylized simulation. These liquidation percentages are conditional on its fixed parameters, not empirical estimates or proof of a general causal magnitude. The three illustrated paths use their full stored price-gap and capital ranges; the table summarizes separate fixed simulated paths."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(fl), FadeIn(fll), FadeIn(side[0]), FadeIn(src))
            self.add(Pth)
            vo.wait_until("a")
            self.play(k.animate.set_value(T), run_time=max(vo.until("b") - 0.5, 4.0), rate_func=linear)
            Pth.clear_updaters()
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        Pth.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def ltcm(self):
        c = crisis_card(
            r"1998", r"Long-Term Capital Management",
            r"Founded in 1994, LTCM ran convergence trades: reported net annual returns of 20\%, 43\%, 41\% and 17\% in 1994--97. Reported assets of \$129bn against \$4.8bn equity imply about 27 times assets/equity. After Russia\'s default it lost 44\% in August 1998. On 23 September, fourteen firms convened by the New York Fed provided \$3.625bn for 90\% of the fund; no Federal Reserve money was used.",
            stats=[(r"\$4.8\text{bn}", r"equity capital, 1 Jan.\ 1998"), (r"\$129\text{bn}", r"balance-sheet "
                                                                                           r"assets, end 1997"),
                   (r"\$1.3\text{tn}", r"OTC derivatives notional, end 1997")],
            width=11.4, font_size=23)
        c.move_to(UP * 0.2)
        src = note(r"Federal Reserve History, ``Near failure of Long-Term Capital Management''; President's Working "
                   r"Group on Financial Markets, \textit{Hedge Funds, Leverage, and the Lessons of LTCM} (April 1999)",
                   font_size=16, color=GREY_B).to_corner(DR, buff=0.2)
        with self.voiceover(
            "The crisis file: Long-Term Capital Management, founded in 1994 by John Meriwether, "
            "returned twenty, forty-three, forty-one and seventeen percent, trading spreads it "
            "expected to converge. The President's Working Group reported four point eight billion "
            "dollars of equity at the start of 1998 against a hundred and twenty-nine billion of "
            "assets, about twenty-seven times assets to equity. <bookmark mark='a'/> After Russia's default, spreads "
            "widened; it lost forty-four percent in August. On the twenty-third of September fourteen "
            "firms, convened by the New York Fed, put up three point six billion for ninety percent "
            "of the fund. No Fed money was used. Part forty-one tells the story."
            " The lesson for this part: every convergence trade is a no-arbitrage argument with a "
            "funding assumption hidden inside it."
        ) as vo:
            self.play(FadeIn(c, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(c.stats, color=ARB, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"A trade converges with certainty. What single comparison decides whether it can still ruin "
                        r"you?")
        with self.voiceover(
            "Pause and predict. A trade is certain to converge. What decides whether it can still "
            "ruin you? <bookmark mark='a'/> Your funding horizon against the time to convergence, "
            "given the losses on the way."
            " Last, the frontier."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"how long your funding lasts against how long convergence takes, given "
                                                r"the losses on the way")))
        self.wait(0.4)
        self.clear_scene()
