from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import crisis as C
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, house_lab,
                                         load)


def _t(d):
    d = np.array([int(str(x).replace("-", "")[:8]) for x in d])
    return (d // 10000) + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


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
                    rf"{h['days2']:.1f} days: it can")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> The worst day of twenty oh eight for the American market was "
            f"the first of December: {100 * -h['worst']:.2f} percent. Assume the whole book moves like the market. "
            f"<bookmark mark='b'/> At two times, equity of one falls to {s2['equity']:.2f}. <bookmark mark='c'/> With the "
            "margin doubled from a quarter to a half, the broker will finance at most twice that. "
            f"<bookmark mark='d'/> So the House must sell {100 * s2['sale_frac']:.0f} percent of its book. If each "
            "position is half a day's volume, at a tenth of the volume that takes about "
            f"{h['days2']:.1f} days. It can."
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
        with self.voiceover("Chapter eleven. The House's forty-first rule belongs to its treasury and funding desk. Every "
                            "crisis in this part ended a firm that was solvent on paper and could not fund itself for a "
                            "week. The rule is a liquidity stress test, run every day."):
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
        dot = Dot(ax.c2p(h["lev_max"], h["s2"]["sale_frac"]), color=QC.HOUSE, radius=0.08)
        leg = legend([(cols[k], names[k]) for k in ("1.0", "2.0", "3.0")], font_size=17)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "The House's stress, by leverage. <bookmark mark='a'/> With margins unchanged, the worst day forces no sale "
            "below about three times. <bookmark mark='b'/> Doubled, the forced sale starts just under two times and "
            "climbs steeply. Tripled, it is steeper still. <bookmark mark='c'/> The dashed line is what the House can sell in a "
            "day at a tenth of volume, with positions of half a day's volume each. <bookmark mark='d'/> The doubled "
            f"curve crosses it just past {h['lev_max']:.0f} times: the House's leverage limit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0][0]))
            vo.wait_until("a")
            self.play(Create(lines["1.0"]), run_time=1.5)
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
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
            "Now through the whole of twenty oh eight and oh nine, day by day, on the market's real returns, at two times. "
            "Two ways a broker can set margin. <bookmark mark='a'/> Linked to recent volatility: "
            f"{100 * h['h0']:.0f} percent in calm markets, rising with RiskMetrics volatility. The House is forced to sell "
            f"{p2['pro_sold']:.2f} times its starting equity over the two years, {pct_fall:.0f} percent of it before the "
            "March twenty oh nine low. "
            "<bookmark mark='b'/> Or set through the cycle, high enough for a stressed year from the start: "
            f"{100 * h['h_ttc'][0]:.0f} percent, which at two times never binds. No forced sale at all. "
            "<bookmark mark='c'/> And notice the twist. The forced seller ended with more equity, "
            f"{p2['pro_end']:.2f} against {p2['ttc_end']:.2f}: selling into a fall protects the seller."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Create(a), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(b), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(stats_))
        self.wait(0.4)
        self.clear_scene()

    def externality(self, h):
        cards = VGroup(
            desk_question(r"privately prudent", r"each forced seller cut its losses: the procyclical margin protected the "
                          r"broker and, here, the fund", width=12.4, font_size=19),
            desk_question(r"socially costly", r"but the House is a price-taker in this sketch; when every levered holder "
                          r"sells together, the sales are the fall: Chapter 2's spiral and Chapter 3's fire sale", width=12.4,
                          font_size=19),
            desk_question(r"the externality", r"no seller counts the loss its sale imposes on others' collateral "
                          r"(Lorenzoni 2008; Stein 2012): why EU rules now require anti-procyclical margin at "
                          r"central counterparties", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Which is the whole problem of this part, in one result. <bookmark mark='a'/> For each firm, selling into a "
            "fall is prudent: the volatility-linked margin protected the broker, and here the fund. "
            "<bookmark mark='b'/> But the House is a price-taker in this sketch. When every levered holder sells "
            "together, their sales are the fall. <bookmark mark='c'/> No seller counts the loss its sale imposes on "
            "everyone else's collateral, as Lorenzoni and Stein formalised. That is why European central counterparties "
            "must now limit how far their margins can swing with volatility."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def rule(self, h):
        rows = [cmath(r"\text{1. leverage}", r"\le", rf"{h['lev_max']:.0f}\times\ \text{{gross}}", font_size=40,
                      colors={r"\text{1. leverage}": LEV_C}),
                cmath(r"\text{2. term funding}", r":", r"\text{margin locked for 30 days, at three or more brokers}", font_size=34,
                      colors={r"\text{2. term funding}": FUND_C}),
                cmath(r"\text{3. cash buffer}", r"\ge", r"\text{the extra margin if it doubled}", font_size=38,
                      colors={r"\text{3. cash buffer}": SAFE_C}),
                cmath(r"\text{4. no single door}", r":", r"\text{no position above half a day's volume}", font_size=36,
                      colors={r"\text{4. no single door}": SPIRAL_C})]
        whys = [why(r"so that the worst day on record, with margins doubled, forces no sale the House cannot make in a day"),
                why(r"a broker that can raise margin overnight is a run waiting to happen: Bear Stearns, Lehman, Archegos"),
                why(r"held in Treasury bills and cash, not in the positions it is meant to protect"),
                why(r"China's limit-down days and Archegos's blocks: a position you cannot sell is not liquid at any price")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "So the forty-first rule has four parts. <bookmark mark='a'/> Gross leverage of at most "
            f"{h['lev_max']:.0f} times: the level at which the worst day on record, with margins doubled, forces no sale the "
            "House cannot make in a day. <bookmark mark='b'/> Term funding: margin terms locked for at least thirty days, "
            "at three or more brokers. <bookmark mark='c'/> A cash buffer at least as large as the extra margin if it "
            "doubled. <bookmark mark='d'/> And no single door: no position larger than half a day's volume."
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
            "The House's code. The forced sale is four lines: the loss, the new equity, the most the lender will "
            "finance, and the difference. The daily path adds the return, then sets the book to the smaller of the "
            "target and what the margin allows, and books the difference as forced."
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Diamond--Dybvig and the run threshold", C.dd_payoffs, "sold = f * c1 / r", 3,
                         extra=((C.run_threshold, "def gap(th):", 3),), width=10.6)
        with self.voiceover(
            "And Chapter ten's run. The payoffs: the bank sells f over r units to pay those who leave, pays them in full "
            "while it can, and shares what is left among those who wait. The threshold is the root of the average gap "
            "between waiting and running, with the share running uniform: the global-games result in three lines."
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
        rule = wrapped_label(r"Rule 41: every day the House replays its worst day on record with margins doubled; its "
                             r"leverage, its funding terms, its cash and its position sizes must survive it without a sale "
                             r"it cannot make in a day.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds to the House's crisis module. <bookmark mark='a'/> Leverage and margin; fire sales "
            "and networks; systemic risk and runs. <bookmark mark='b'/> And the forty-first rule. Every day the House "
            "replays its worst day on record with margins doubled. Its leverage, funding terms, cash and position sizes "
            "must survive it without a sale it cannot make in a day."
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
