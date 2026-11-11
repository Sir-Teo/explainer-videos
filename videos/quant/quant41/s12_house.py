from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from explainer.quant.house import crisis as C
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, house_lab,
                                         load)


def _t(d):
    from videos.quant.quant41.common import calendar_year
    return calendar_year(d)


class House(VoiceoverScene):
    def construct(self):
        h = load("house")
        self.answer(h)
        self.card()
        self.sweep(h)
        self.archegos(h)
        self.path(h)
        self.externality(h)
        self.rule(h)
        self.lab()
        self.lab2()
        self.module()
        self.test()

    def answer(self, h):
        s2 = h["s2"]
        rows = [cmath(r"\text{worst day of 2008}", r":", rf"{100 * h['worst']:.2f}\%", font_size=38,
                      colors={r"\text{worst day of 2008}": BAD}),
                cmath(r"\text{equity}", r":", rf"1 \to {s2['equity']:.2f},\ \text{{assets}}\ 2 \to {s2['assets']:.2f}",
                      font_size=38, colors={r"\text{equity}": LEV_C}),
                cmath(r"\text{margin } 25\% \to 50\%", r":", rf"\text{{assets at most }} {s2['equity']:.2f}/0.5 = "
                      rf"{s2['max_assets']:.2f}", font_size=36, colors={r"\text{margin } 25\% \to 50\%": FUND_C}),
                cmath(r"\text{sell}", r":", rf"{s2['sale']:.2f} = {100 * s2['sale_frac']:.0f}\%\ \text{{of the book}}",
                      font_size=40, colors={r"\text{sell}": SPIRAL_C})]
        whys = [why(r"the US market's return on 1 December 2008, from Kenneth French's daily file: the stress assumes the "
                    r"whole book moves like the market"),
                why(r"at two times, the day costs twice the market's fall"),
                why(r"a prime broker that doubles its margin halves the leverage it will finance"),
                why(r"a tenth of the book; if each position is half a day's volume, selling it at 10\% of volume takes "
                    rf"{h['days2']:.1f} volume-equivalent days; execution under stress is not guaranteed")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""The chosen public-market stress. <bookmark mark='a'/> The worst market return within two thousand eight occurs on December first, a {100 * -h['worst']:.2f} percent fall. This assumes the entire teaching book moves like that market, not a sealed strategy's realized path. <bookmark mark='b'/> At two times, equity one becomes {s2['equity']:.2f}. <bookmark mark='c'/> A fifty-percent haircut caps assets at twice that equity. <bookmark mark='d'/> The required sale is {100 * s2['sale_frac']:.0f} percent of remaining assets. Positions equal to half a normal day's volume imply {h['days2']:.1f} volume-equivalent days at ten-percent participation. Actual depth, prices, volume and trading halts can prevent execution. This calculation is not a liquidity certificate."""
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def card(self):
        c = chapter_card(11, r"Rule 41: survive the margin call you have not been sent", r"How much leverage can the House "
                         r"carry through a crisis?", part=PART)
        with self.voiceover('Chapter eleven. A proposed treasury and funding rule for a teaching book. Its inputs here are ordinary public market returns and chosen financing assumptions. It does not read a sealed strategy outcome, certify live positions, or establish actual broker commitments. The exercise asks what a specified loss and haircut shock would require, and where the assumed ability to sell can fail.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sweep(self, h):
        sw = h["sweep"]
        lev = np.array([x["lev"] for x in sw])
        g = axes([1, 8], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"gross leverage before the day, $\lambda$",
                 ylabel=r"share of the book that must be sold", xticks=[1, 2, 3, 4, 5, 6, 7, 8], yticks=[0, 0.5, 1],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        cols = {"1.0": SAFE_C, "2.0": HURDLE, "3.0": BAD}
        names = {"1.0": r"margin unchanged, 25\%", "2.0": r"doubled, 50\%", "3.0": r"tripled, 75\%"}
        lines = {k: curve(ax, lev, np.array([x[k] for x in sw]), cols[k], stroke_width=3) for k in ("1.0", "2.0", "3.0")}
        lim = h["part"] / h["pos_adv"]
        cap = DashedLine(ax.c2p(1, lim), ax.c2p(8, lim), color=GREY_C, stroke_width=1.5)
        cap_l = label(r"a day's selling at 10\% of volume", font_size=15, color=GREY_B).next_to(ax.c2p(8, lim), UP,
                                                                                           buff=0.08).align_to(cap, RIGHT)
        selected = next(row for row in sw if row["lev"] == h["lev_max"])
        dot = Dot(ax.c2p(h["lev_max"], selected["2.0"]), color=QC.HOUSE, radius=0.08)
        leg = legend([(cols[k], names[k]) for k in ("1.0", "2.0", "3.0")], font_size=17)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"""The same chosen stress across a fixed leverage grid. <bookmark mark='a'/> At a twenty-five-percent initial haircut, leverage above four is already infeasible for this single-book model; the extended curves illustrate hypothetical post-shock funding requirements. <bookmark mark='b'/> A fifty-percent or seventy-five-percent final haircut increases required sales. <bookmark mark='c'/> The dashed line is a chosen volume-equivalent day's sale, assuming ten-percent participation and half-a-day positions. It is not guaranteed stressed capacity. <bookmark mark='d'/> The largest tested quarter-step leverage satisfying the doubled-haircut arithmetic is {h['lev_max']:.2f}. The dot uses that row's actual sale fraction. This discrete maximum is not an exactly solved continuous limit or an approved live leverage ceiling."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0][0]), Create(lines['1.0']))
            vo.wait_until("a")
            self.play(Indicate(lines['1.0'], color=HURDLE), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0][1]), Create(lines["2.0"]), FadeIn(side[0][2]), Create(lines["3.0"]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cap), FadeIn(cap_l))
            vo.wait_until("d")
            self.play(FadeIn(dot, scale=1.5))
        self.wait(0.4)
        self.clear_scene()

    def archegos(self, h):
        s5 = h["s5"]
        cards = VGroup(
            desk_question(r"Archegos, March 2021", r"a family office with concentrated positions held through total-return "
                          r"swaps at several prime brokers, each seeing only its own slice, as reported", width=12.4,
                          font_size=19),
            desk_question(rf"the same stress at 5$\times$, positions five days' volume",
                          rf"sell {100 * s5['sale_frac']:.0f}\% of the book: {h['days5']:.0f} days at a tenth of volume",
                          width=12.4, font_size=19),
            desk_question(r"what happened", r"when one stock fell, the banks sold blocks in a race; Credit Suisse reported "
                          r"a \$5.5bn loss; its founder was later convicted of fraud", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Against a real case. <bookmark mark='a'/> Archegos, a family office, held concentrated positions through "
            "total-return swaps at several prime brokers, each seeing only its own slice, as reported: LTCM's lesson, "
            "unlearned. <bookmark mark='b'/> Run the House's stress at five times, with positions of five days' volume: "
            f"sell {100 * s5['sale_frac']:.0f} percent of the book, which would take {h['days5']:.0f} days. "
            "<bookmark mark='c'/> In March twenty twenty-one, when one of its stocks fell, the banks did not wait. They "
            "sold blocks in a race to be first; Credit Suisse reported a loss of five and a half billion dollars; the "
            "founder was later convicted of fraud."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def path(self, h):
        t = _t(h["d"])
        p2 = h["paths"]["2.0"]
        pct_fall = 100 * p2["pro_fall_share"]
        g = axes([2008, 2010], [0, 1.1], x_length=7.6, y_length=4.2, xlabel=r"2008--2009, daily",
                 ylabel=r"equity of a 2$\times$ book, start = 1", xticks=[2008, 2009, 2010], yticks=[0, 0.5, 1.0],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        a = curve(ax, t, np.asarray(p2["pro_eq"], float), BAD, stroke_width=2.5)
        b = curve(ax, t, np.asarray(p2["ttc_eq"], float), SAFE_C, stroke_width=2.5)
        leg = legend([(BAD, r"margin linked to volatility"), (SAFE_C, r"margin set through the cycle")], font_size=17)
        stats_ = VGroup(
            label(rf"forced sales: {p2['pro_sold']:.2f} and {p2['ttc_sold']:.2f} times starting equity", font_size=16, color=GREY_A),
            label(rf"lowest equity: {p2['pro_min']:.2f} and {p2['ttc_min']:.2f}", font_size=16, color=GREY_A),
            label(rf"at the end of 2009: {p2['pro_end']:.2f} and {p2['ttc_end']:.2f}", font_size=16, color=GREY_A))
        stats_.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(leg, stats_).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"""A descriptive simulation on public market returns in two thousand eight and nine, with target leverage two. <bookmark mark='a'/> Volatility-linked haircuts produce {p2['pro_sold']:.2f} times starting equity in haircut-attributable sales. That statistic excludes ordinary target-leverage turnover. The book can re-lever toward its target after gains. <bookmark mark='b'/> The fixed haircut is {100 * h['h_ttc'][0]:.0f} percent, chosen from half a multiplier based on a pre-two-thousand-eight ninety-ninth-percentile volatility estimate, with the coded floor and cap. This creates different headroom; it is not the same funding budget under a controlled intervention. <bookmark mark='c'/> End equity is {p2['pro_end']:.2f} versus {p2['ttc_end']:.2f} for this window. That path-specific ordering does not prove forced selling is beneficial or that either policy protects a broker in general."""
        ) as vo:
            self.play(FadeIn(g), Create(a))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Indicate(a, color=HURDLE), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(b), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(stats_))
        self.wait(0.4)
        self.clear_scene()

    def externality(self, h):
        cards = VGroup(
            desk_question(r"privately prudent", 'in this chosen path, reduced exposure changes later returns; the comparison does not isolate a causal margin-policy or broker-protection effect', width=12.4, font_size=19),
            desk_question(r"socially costly", r"but the House is a price-taker in this sketch; when every levered holder "
                          r"sells together, the sales are the fall: Chapter 2's spiral and Chapter 3's fire sale", width=12.4,
                          font_size=19),
            desk_question(r"the externality", r"no seller counts the loss its sale imposes on others' collateral "
                          r"(Lorenzoni 2008; Stein 2012): why EU rules now require anti-procyclical margin at "
                          r"central counterparties", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Private incentives and external effects. <bookmark mark='a'/> Our price-taking path comparison shows a particular equity ordering, not a general benefit from forced selling or proof that a broker avoided loss. <bookmark mark='b'/> Once many holders have price impact, their liquidations can depress collateral values and induce others' sales; this path simulator itself does not estimate that feedback. <bookmark mark='c'/> Models by Lorenzoni and Stein formalize settings where private decisions omit such effects. Anti-procyclicality tools are motivated by these concerns, but applicable requirements and their effects depend on institutions, contracts and historical rules."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def rule(self, h):
        rows = [cmath(r"\text{1. leverage}", r"\le", rf"{h['lev_max']:.2f}\times\ \text{{gross}}", font_size=40,
                      colors={r"\text{1. leverage}": LEV_C}),
                cmath(r"\text{2. term funding}", r":", '\\text{reviewed term funding; several counterparties}', font_size=34,
                      colors={r"\text{2. term funding}": FUND_C}),
                cmath(r"\text{3. cash buffer}", r"\ge", r"\text{the extra margin if it doubled}", font_size=38,
                      colors={r"\text{3. cash buffer}": SAFE_C}),
                cmath(r"\text{4. no single door}", r":", r"\text{no position above half a day's volume}", font_size=36,
                      colors={r"\text{4. no single door}": SPIRAL_C})]
        whys = [why('the largest tested leverage passing this chosen 2008-day/volume arithmetic; not a continuous bound or an execution guarantee'),
                why(r"a broker that can raise margin overnight is a run waiting to happen: Bear Stearns, Lehman, Archegos"),
                why(r"held in Treasury bills and cash, not in the positions it is meant to protect"),
                why(r"China's limit-down days and Archegos's blocks: a position you cannot sell is not liquid at any price")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""A proposed four-part research rule. <bookmark mark='a'/> Use {h['lev_max']:.2f} as the largest passing tested leverage under this specified two-thousand-eight shock, haircut and normal-volume arithmetic; examine further scenarios before any live limit. <bookmark mark='b'/> Seek legally and operationally reviewed term funding and counterparty diversification. No actual thirty-day margin lock is established here. <bookmark mark='c'/> Hold a separately defined liquidity buffer against additional collateral needs. <bookmark mark='d'/> Limit positions relative to stressed executable depth, rather than treating average volume as a promise. The proposal requires contract, execution and risk review before deployment."""
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The forced sale", C.deleverage, "a1 = assets * (1 - loss_frac)", 4,
                         extra=((C.margin_path, "E += A * r[t]", 2), (C.margin_path, "target = lev * E", 4)), width=10.6)
        with self.voiceover(
            'The unchanged crisis library. The forced-sale function marks assets and equity, computes an equity-over-haircut cap and sells the positive excess. In the daily path, assets are reset to the smaller of target-leverage assets and the collateral cap; gains can lead to re-levering. The recorded forced amount is only the haircut-attributable reduction relative to the target, not all purchases and sales. We disclose those semantics rather than changing the financial algorithm.'
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Diamond--Dybvig and the run threshold", C.dd_payoffs, "sold = f * c1 / r", 3,
                         extra=((C.run_threshold, "def gap(th):", 3),), width=10.6)
        with self.voiceover(
            'The chosen run-game code computes early and waiting payoffs, including the zero waiting branch after assets are exhausted. It averages wait-minus-run under a uniform rank belief, then numerically finds a threshold. The assumed flat local prior, payoff structure and insured non-running share are essential. These few lines illustrate a particular limiting construction; they do not prove general global-games uniqueness or model a recourse central-bank loan as a change in asset payoff.'
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("treasury",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{deleverage}, \texttt{spiral}, \texttt{margin\_path}", r"leverage and margin"),
            (r"\texttt{glt\_firesale}, \texttt{eisenberg\_noe}, \texttt{senior\_clearing}", r"fire sales and networks"),
            (r"\texttt{covar}, \texttt{mes}, \texttt{srisk}, \texttt{dd\_payoffs}, \texttt{run\_threshold}", r"systemic risk and runs"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label('Proposed Rule 41: combine specified loss/haircut stresses, executable-depth analysis, funding review and a separate cash buffer; the chosen grid exercise alone does not approve live leverage.', 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The crisis module supplies teaching tools. <bookmark mark='a'/> Leverage and margin, common-asset price impact, network clearing, systemic proxies and chosen run-game payoffs. These functions have different assumptions and are not one fitted crisis predictor. <bookmark mark='b'/> Proposed Rule forty-one combines stress arithmetic with funding, cash and executable-depth review. The ordinary public-return illustration neither accesses a sealed strategy nor establishes that any live book can liquidate within a day."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"a fund that says it is market-neutral", r"ask what it must sell if its margins double tomorrow, "
                          r"and how many days that takes (Chapter 11)", width=12.0, font_size=19),
            desk_question(r"a bank whose bonds are held to maturity", r"ask what they are worth today, and how much of its "
                          r"funding can leave in a day (Chapter 10)", width=12.0, font_size=19),
            desk_question(r"a network that looks well diversified", r"ask how large a shock it is diversified against: "
                          r"past the threshold, links spread losses instead of sharing them (Chapter 4)", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three tests to carry away. <bookmark mark='a'/> When a fund says it is market-neutral, ask what it must sell "
            "if its margins double tomorrow, and how many days that takes. <bookmark mark='b'/> When a bank holds bonds "
            "to maturity, ask what they are worth today, and how much of its funding can leave in a day. "
            "<bookmark mark='c'/> And when a network looks well diversified, ask against how large a shock: past the "
            "threshold, the links spread losses instead of sharing them."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()
