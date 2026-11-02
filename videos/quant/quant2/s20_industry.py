from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, CCP, LOSS, PART, RATE, TRADE, load, node

BOXES = {"retail": (r"retail investors", (-5.4, 2.4), GREY_B), "broker": (r"retail broker", (-2.4, 2.4), TRADE),
         "whole": (r"wholesaler", (0.6, 2.4), TRADE), "exch": (r"exchange", (0.6, 0.6), TRADE),
         "ccp": (r"clearing house", (3.6, 0.6), CCP), "cust": (r"custodian", (5.6, 2.4), CCP),
         "fund": (r"hedge fund", (-5.4, -1.6), QC.IDEA), "pb": (r"prime broker", (-2.4, -1.6), CASH),
         "repo": (r"repo lender (money fund)", (0.9, -1.6), RATE)}
FLOWS = [("broker", "retail", r"zero commission"), ("whole", "broker", r"PFOF"), ("retail", "broker", r"orders"),
         ("broker", "whole", r"orders"), ("exch", "ccp", r"trades"), ("ccp", "cust", r"settlement"),
         ("fund", "pb", r"fees, financing"), ("pb", "repo", r"collateral"), ("repo", "pb", r"cash"),
         ("pb", "exch", r"hedges"), ("fund", "exch", r"orders")]

ROLES = [(r"quant researcher", r"finds and tests signals and models"),
         (r"quant trader", r"runs strategies, sizes risk, decides when to stop"),
         (r"quant developer", r"builds the data, the backtester, the trading systems"),
         (r"risk quant", r"models what can go wrong, sets limits"),
         (r"strat / desk quant", r"prices and hedges for a bank's trading desk"),
         (r"structurer", r"designs products for clients (Part 15)")]

MAP = [(r"HFT and market making", 0, 0, r"Citadel Securities, Virtu, Jane Street, Optiver, XTX"),
       (r"options market making", 0.6, 1, r"SIG (Susquehanna), Optiver"),
       (r"statistical arbitrage", 1.5, 0, r"many multi-strategy pods"),
       (r"CTAs and trend", 2.6, 2, r"Man AHL"),
       (r"systematic equity", 2.9, 0, r"AQR, Two Sigma"),
       (r"multi-manager platforms", 2.2, 3, r"Millennium, Citadel"),
       (r"bank desks", 3.4, 1, r"pricing, hedging, structuring, XVA")]


class Industry(VoiceoverScene):
    def construct(self):
        ind = load("industry")
        self.card()
        self.money_map()
        self.firms(ind)
        self.regulators(ind)
        self.quant_map()

    def card(self):
        c = chapter_card(17, r"Industry: who runs the machine", r"Who earns what from the plumbing, by their own "
                         r"disclosures?", lit=(1990, 2000), part=PART)
        with self.voiceover("Chapter seventeen. The industry: who runs the machine, and how they earn."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def money_map(self):
        nodes = {}
        for k, (t, (x, y), col) in BOXES.items():
            nodes[k] = node(t, col, width=2.3, height=0.8, font_size=19).move_to([x, y, 0])
        arrows, particles = VGroup(), VGroup()
        tr = ValueTracker(0)
        for i, (a, b, t) in enumerate(FLOWS):
            pa, pb = nodes[a].get_center(), nodes[b].get_center()
            off = np.array([-(pb - pa)[1], (pb - pa)[0], 0])
            off = 0.12 * off / (np.linalg.norm(off) + 1e-9)
            ln = Line(pa + off, pb + off, buff=0.5, color=GREY_D, stroke_width=1.5)
            arrows.add(VGroup(ln, label(t, font_size=15, color=GREY_B).move_to(ln.get_center() + 2.2 * off)))

            def mk(ln=ln, i=i):
                return VGroup(*[Dot(ln.point_from_proportion((tr.get_value() * 0.5 + j / 3 + i * 0.07) % 1),
                                    radius=0.045, color=QC.IDEA) for j in range(3)])
            particles.add(always_redraw(mk))
        with self.voiceover(
            "The money map: who pays whom. Retail orders go to a commission-free broker; the wholesaler that fills them pays "
            "for the flow. Exchange trades are novated to the clearing house and settled at the custodian. Hedge funds pay "
            "their prime broker, which funds itself in repo against their collateral. <bookmark mark='a'/> Every arrow is a "
            "revenue line. Open the boxes, using only what firms and regulators have published."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n) for n in nodes.values()], lag_ratio=0.1), FadeIn(arrows))
            self.add(particles)
            self.play(tr.animate.set_value(3), run_time=8, rate_func=linear)
            vo.wait_until("a")
            self.play(tr.animate.set_value(4), run_time=2, rate_func=linear)
        particles.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def firms(self, ind):
        c1 = firm_card(r"CME Group", r"Futures and options exchange and clearing house: earns per contract traded and "
                       r"cleared, plus market data.", numbers=[(rf"\${ind['cme_rev_2024_bn']}\,\text{{bn}}",
                                                               r"record revenue, 2024"),
                                                              (rf"{ind['cme_adv_2024_m']}\,\text{{m}}",
                                                               r"contracts a day, 2024")],
                       source=r"CME Group, 2024 results (February 2025)", width=6.2, font_size=19)
        c2 = firm_card(r"Virtu Financial", r"Market maker and wholesaler: earns the spread, less what it pays for "
                       r"flow and to venues.", numbers=[(rf"\${ind['virtu_rev_2024_m']:,.1f}\,\text{{m}}".replace(",", "{,}"),
                                                         r"revenue 2024 (+25.4\%)"),
                                                        (rf"\${ind['virtu_ni_2024_m']}\,\text{{m}}", r"net income")],
                       source=r"Virtu, 2024 Form 10-K", width=6.2, font_size=19)
        c3 = firm_card(r"Robinhood", r"Retail broker: no commission; paid per contract for options orders and from "
                       r"the spread for equities (its 10-K's terms), plus interest on cash.",
                       numbers=[(rf"\${ind['hood_q4_tx_m']}\,\text{{m}}", r"transaction revenue, Q4 2024"),
                                (rf"\${ind['hood_q4_crypto_m']} / {ind['hood_q4_options_m']} / {ind['hood_q4_equities_m']}"
                                 r"\,\text{m}", r"crypto / options / equities")],
                       source=r"Robinhood, Q4 2024 results; 2024 Form 10-K", width=6.2, font_size=19)
        c4 = firm_card(r"Citadel Securities", r"Wholesaler and market maker. Says it executes more than a third of US "
                       r"retail equity volume (a company claim); nearly half of internalized GameStop volume in "
                       r"January 2021 (SEC).", numbers=[(r">35\%", r"of US retail volume (company)")],
                       source=r"company website; SEC staff report (2021)", width=6.2, font_size=19)
        grid = VGroup(VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(c3, c4).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.4:
            grid.scale_to_fit_height(7.4)
        with self.voiceover(
            f"CME Group, the largest futures exchange, which clears what it trades, reported record 2024 revenue of "
            f"{ind['cme_rev_2024_bn']} billion dollars on about {ind['cme_adv_2024_m']:.0f} million contracts a day. "
            f"<bookmark mark='a'/> Virtu, a wholesaler and market maker, earned about {ind['virtu_rev_2024_m'] / 1000:.1f} "
            f"billion in revenue, up a quarter, and {ind['virtu_ni_2024_m']:.0f} million of net income. <bookmark mark='b'/> "
            f"Robinhood charges no commission; of its {ind['hood_q4_tx_m']} million dollars of transaction revenue in the last "
            f"quarter of 2024, {ind['hood_q4_crypto_m']} came from crypto, {ind['hood_q4_options_m']} from options and only "
            f"{ind['hood_q4_equities_m']} from stocks: payment for order flow is an options business. <bookmark mark='c'/> "
            "And Citadel Securities says it executes more than a third of American retail volume: the company's own claim."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(c4, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def regulators(self, ind):
        c1 = firm_card(r"Hedge funds and the basis trade", r"Long Treasuries, short Treasury futures, funded in repo: "
                       r"chapter two's carry trade on the safest asset, at many times leverage.",
                       numbers=[(rf"\sim\${ind['basis_trade_bn']}\,\text{{bn}}", r"basis trade, September 2025"),
                                (rf"\${ind['hf_repo_tn']:.1f}\,\text{{tn}}", r"hedge-fund repo borrowing")],
                       source=r"Monin, FEDS Notes (22 June 2026); Glicoes et al.\ (2024)", width=6.2, font_size=19)
        c2 = firm_card(r"Regulators", r"SEC: Rule 612, Treasury clearing (cash trades by 31 December 2026, repo by 30 "
                       r"June 2027). FCA: the LME fine. SEBI: F\&O studies; on 3 July 2025 an \textit{interim} order "
                       r"against Jane Street \textit{alleging} manipulation of index options around expiries, with "
                       r"Rs\,4,843.57 crore impounded into escrow. Jane Street disputes the findings; the case is "
                       r"pending.", numbers=[], source=r"SEC; FCA final notice (March 2025); SEBI interim order "
                       r"(3 July 2025)", width=6.2, font_size=19)
        pair = VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        with self.voiceover(
            "Prime brokers' biggest recent trade is chapter two's carry on Treasuries: buy the bond, sell the future, fund it "
            f"in repo, many times over. A Federal Reserve note puts it near {ind['basis_trade_bn']} billion dollars in "
            f"September 2025, with hedge funds borrowing {ind['hf_repo_tn']:.0f} trillion in repo. <bookmark mark='a'/> "
            "Regulators set the rules. The SEC is moving Treasuries into central clearing, cash trades by the end of 2026 and "
            "repo by mid-2027. India's SEBI issued an interim order in July 2025 alleging that Jane Street manipulated index "
            "options around expiry days, and impounded about four thousand eight hundred crore rupees in escrow. Those are "
            "allegations in an interim order; Jane Street disputes them, and the case is pending."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def quant_map(self):
        g = axes([-0.3, 3.9], [-0.5, 3.6], x_length=7.4, y_length=4.6, xlabel=r"holding horizon",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: ["\\mu s", "\\text{minutes}", "\\text{days}", "\\text{months}"][int(v)],
                 font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        ylab = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(-0.3, y), LEFT, buff=0.1)
                        for t, y in ((r"equities", 0), (r"options", 1), (r"futures", 2), (r"everything", 3))])
        blobs = VGroup()
        for name, x, y, who in MAP:
            blobs.add(VGroup(Dot(ax.c2p(x, y), radius=0.12, color=QC.IDEA),
                             label(name, font_size=17, color=QC.IDEA).next_to(ax.c2p(x, y), UP, buff=0.1),
                             label(who, font_size=14, color=GREY_B).next_to(ax.c2p(x, y), DOWN, buff=0.1)))
        roles = VGroup(label(r"The roles", font_size=26, color=QC.HOUSE))
        for r_, what in ROLES:
            roles.add(VGroup(label(r_, font_size=20, color=QC.HOUSE), label(what, font_size=16, color=GREY_A))
                      .arrange(DOWN, aligned_edge=LEFT, buff=0.03))
        roles.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.4)
        q = desk_question(r"Make me a market on the number of trading days in a US year.", width=5.0, font_size=19)
        q.to_corner(DR, buff=0.2)
        with self.voiceover(
            "Where do quants fit in this machine? Place the firms by how long they hold a position and what they trade. At "
            "microseconds, the high-frequency market makers and wholesalers. Options market makers a little slower. "
            "Statistical arbitrage over minutes to days; trend followers and systematic equity over weeks to months; the "
            "multi-manager platforms across all of it; and the banks' desks pricing and hedging for clients. Each has its parts "
            "later in the series. <bookmark mark='a'/> And the jobs: the researcher who finds and tests ideas, the trader who "
            "runs them and decides when to stop, the developer who builds the systems, the risk quant who asks what can go "
            "wrong, the desk quant who prices and hedges for a bank, and the structurer who designs products. Their interviews "
            "open with questions like this one: make me a market on the number of trading days in a year."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ylab), LaggedStart(*[FadeIn(b) for b in blobs], lag_ratio=0.4, run_time=6))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in roles], lag_ratio=0.3, run_time=4))
            self.play(FadeOut(roles), FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
