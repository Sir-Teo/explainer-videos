from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, GAIN, LOSS, PART, TRADE, lab, load

C_ = {r"D(p)": GAIN, r"S(p)": LOSS, r"V(p)": QC.IDEA}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Auction(VoiceoverScene):
    def construct(self):
        a = load("auction")
        al = load("auction_live")
        self.card()
        self.live(a, al)
        self.proof()
        self.moc(a, al)
        self.close_lab(a)

    def card(self):
        c = chapter_card(4, r"Auctions: one price for everyone", r"Which price clears the most shares?", part=PART)
        with self.voiceover("Chapter four. Auctions: one price for everyone."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def live(self, a, al):
        bp, bq = np.asarray(a["bid_px"]), np.asarray(a["bid_qty"])
        ap, aq = np.asarray(a["ask_px"]), np.asarray(a["ask_qty"])
        order, side = np.asarray(al["order"]), np.asarray(al["side"])
        nb = len(bp)
        grid = np.round(np.arange(98.6, 101.41, 0.02), 2)
        g = axes([98.6, 101.4], [0, 32000], x_length=7.6, y_length=4.3, xlabel=r"price", ylabel=r"shares",
                 xticks=[99, 100, 101], yticks=[0, 10000, 20000, 30000],
                 yfmt=lambda v: f"{v / 1000:.0f}" + r"\text{k}", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        k = ValueTracker(0)

        def curves():
            n = int(k.get_value())
            sel = order[:n]
            bi = sel[sel < nb]
            ai = sel[sel >= nb] - nb
            dm = np.array([bq[bi][bp[bi] >= p].sum() for p in grid])
            sp = np.array([aq[ai][ap[ai] <= p].sum() for p in grid])
            out = VGroup(VMobject(color=GAIN, stroke_width=3.5).set_points_as_corners(
                [ax.c2p(x, y) for x, y in zip(grid, np.minimum(dm, 32000))]),
                VMobject(color=LOSS, stroke_width=3.5).set_points_as_corners(
                [ax.c2p(x, y) for x, y in zip(grid, np.minimum(sp, 32000))]))
            px = al["price"][max(n - 1, 0)] if n > 0 else np.nan
            if np.isfinite(px):
                out.add(DashedLine(ax.c2p(px, 0), ax.c2p(px, 32000), color=QC.IDEA, stroke_width=2))
            return out
        cv = always_redraw(curves)
        pr = np.asarray(al["price"], float)
        vol = np.asarray(al["volume"], float)
        imb = np.asarray(al["imbalance"], float)

        def at(arr):
            n = int(k.get_value())
            v = arr[max(n - 1, 0)]
            return float(v) if np.isfinite(v) else 0.0
        r1 = ro(r"\text{orders in:}", lambda: k.get_value(), digits=0, font_size=28)
        r2 = ro(r"\text{indicative price:}", lambda: at(pr), digits=2, font_size=28, color=QC.IDEA)
        r3 = ro(r"\text{matched:}", lambda: at(vol), digits=0, font_size=28)
        r4 = ro(r"\text{imbalance:}", lambda: at(imb), digits=0, font_size=28, color=GREY_A)
        panel = VGroup(r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        leg = legend([(GAIN, r"demand: bids at this price or higher"), (LOSS, r"supply: asks at this price or lower")],
                     font_size=19).next_to(panel, DOWN, buff=0.5).align_to(panel, LEFT)
        kinds = VGroup(definition_card(r"Uniform price", r"every executed order pays the one clearing price: the "
                                       r"opening and closing auctions", width=4.4, color=QC.IDEA, font_size=19),
                       definition_card(r"Discriminatory price", r"each order pays its own price: the continuous book, "
                                       r"and some bond auctions", width=4.4, color=TRADE, font_size=19))
        keep_in_frame(VGroup(panel, leg), 0.35)
        kinds.arrange(DOWN, buff=0.25).move_to(VGroup(panel, leg)).align_to(panel, UP)
        keep_in_frame(kinds, 0.35)
        note_ = note(r"300 simulated limit orders, arriving in random order; published as imbalance feeds (e.g.\ "
                     r"Nasdaq's NOII)", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Most exchanges open and close the day with a call auction. For a few minutes orders are collected, nothing "
            "trades, and the exchange publishes what would happen if it stopped now: an indicative price, the shares that "
            "would match, and the imbalance left over. <bookmark mark='a'/> Watch three hundred orders arrive one at a time. "
            "Each buy adds a step to the green staircase, the shares wanted at each price or higher; each sell adds a step to "
            "the red one, the shares offered at each price or lower. The indicative price jumps around while the book is thin, "
            f"then settles as it fills, at {a['price']:.2f}. <bookmark mark='b'/> At the end everyone who trades pays the "
            "same price: a uniform-price auction. The continuous book, where each order pays its own price, is "
            "discriminatory."
        ) as vo:
            self.play(FadeIn(g), FadeIn(panel), FadeIn(leg), FadeIn(note_))
            self.add(cv)
            self.play(k.animate.set_value(12), run_time=vo.until("a"), rate_func=linear)
            self.play(k.animate.set_value(60), run_time=4, rate_func=linear)
            self.play(k.animate.set_value(len(order)), run_time=8, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeOut(leg), FadeOut(panel), FadeIn(kinds))
        cv.clear_updaters()
        for m in (r1, r2, r3, r4):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [
            row(r"D(p)", r"=", r"\sum_{b_i \ge p} q_i \ \ \text{falls}, \qquad", r"S(p)", r"=",
                r"\sum_{a_j \le p} q_j \ \ \text{rises}"),
            row(r"V(p)", r"=", r"\min\big(D(p),\ S(p)\big)"),
            row(r"S < D:\ ", r"V(p)", r"=", r"S(p) \uparrow, \qquad S > D:\ ", r"V(p)", r"=", r"D(p)\downarrow"),
            row(r"\max_p", r"V(p)", r"\ \text{ at the crossing } D(p^*) \approx S(p^*)"),
        ]
        whys = [why(r"a higher price loses buyers and gains sellers"),
                why(r"a trade needs both sides: the executable volume is the smaller"),
                why(r"left of the crossing $V$ follows the rising supply; right of it, the falling demand"),
                why(r"so the volume peaks where the staircases cross; ties: least imbalance, then a reference price")]
        for r_ in rows:
            r_.scale(0.9)
        step = ladder(self, rows, whys, keep=4, top=3.1, x=0.0, align_index=None, buff=0.42, edge=6.9)
        head = theorem_card(r"The clearing price maximizes volume", r"For any set of limit orders, the price $p^*$ "
                            r"where demand and supply cross executes the most shares.", width=8.0, font_size=21)
        head.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Why the crossing? Demand at a price p counts the bids at p or higher, so it can only fall as p rises. "
            "Supply counts the asks at p or lower, so it can only rise. <bookmark mark='a'/> At any price the "
            "shares that can actually trade are the smaller of the two. <bookmark mark='b'/> To the left of the "
            "crossing supply is the smaller and rising; to the right, demand is the smaller and falling. "
            "<bookmark mark='c'/> So the volume climbs, then falls, and it peaks where the staircases cross. "
            "When several prices tie, exchanges take the one with the least imbalance, then the one nearest a "
            "reference price."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(head))
        self.wait(0.4)
        self.clear_scene()

    def moc(self, a, al):
        c = np.asarray(a["candidates"])
        dm, sp = np.asarray(a["demand"]), np.asarray(a["supply"])
        cm, dm2 = np.asarray(al["moc_candidates"]), np.asarray(al["moc_demand"])
        m = (c >= 99.4) & (c <= 100.8)
        m2 = (cm >= 99.4) & (cm <= 100.8)
        g = axes([99.4, 100.8], [8000, 22000], x_length=7.2, y_length=4.2, xlabel=r"price", ylabel=r"shares",
                 xticks=[99.5, 100, 100.5], yticks=[10000, 15000, 20000],
                 yfmt=lambda v: f"{v / 1000:.0f}" + r"\text{k}", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax

        def stair(xs, ys, col):
            ys = np.clip(ys, 8000, 22000)
            return VMobject(color=col, stroke_width=3.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
        d0, s0 = stair(c[m], dm[m], GAIN), stair(c[m], sp[m], LOSS)
        d1 = stair(cm[m2], dm2[m2], QC.IDEA)
        p0 = DashedLine(ax.c2p(a["price"], 8000), ax.c2p(a["price"], 22000), color=GREY_B, stroke_width=2)
        p1 = DashedLine(ax.c2p(al["moc_price"], 8000), ax.c2p(al["moc_price"], 22000), color=QC.IDEA, stroke_width=2.5)
        res = VGroup(
            MathTex(rf"\text{{clearing price}}\ {a['price']:.2f} \to {al['moc_price']:.2f}", font_size=30,
                    color=QC.IDEA),
            MathTex(rf"\text{{the same 2{{,}}000 bought in the book: average}}\ {al['walk_avg']:.2f},\ \text{{last}}\ "
                    rf"{al['walk_last']:.2f}", font_size=26),
            wrapped_label(r"Bogousslavsky and Muravyev (\textit{Journal of Financial Markets}, 2023): closing auctions "
                          r"were 7.5\% of US daily volume in 2018, up from 3.1\% in 2010, driven by index funds and "
                          r"ETFs", 5.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        with self.voiceover(
            "Now add one more order: a market-on-close buy of two thousand shares, willing to pay any price. It shifts the "
            "whole demand staircase right by two thousand shares. <bookmark mark='a'/> The crossing moves from "
            f"{a['price']:.2f} to {al['moc_price']:.2f}, and every share in the auction trades there. Bought instead by "
            f"walking the continuous book, the same two thousand shares would have averaged {al['walk_avg']:.2f} and pushed "
            f"the last fill to {al['walk_last']:.2f}. <bookmark mark='b'/> That's why the close matters. Index funds and "
            "many mutual funds are valued at the closing price, so they trade there, in size: Bogousslavsky and Muravyev "
            "measured closing auctions at seven and a half percent of American volume in 2018, up from three percent in "
            "2010. Big orders meet in one place, at one price, and the price that results is the one indices are computed "
            "from."
        ) as vo:
            self.play(FadeIn(g), Create(d0), Create(s0), Create(p0))
            self.play(TransformFromCopy(d0, d1), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(p1), FadeIn(res[0]))
            self.play(FadeIn(res[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[2]))
        self.wait(0.4)
        self.clear_scene()

    def close_lab(self, a):
        card = lab_card(r"the call auction", [
            "def call_auction(bid_px, bid_qty, ask_px, ask_qty):",
            "    cands = np.unique(np.concatenate([bid_px, ask_px]))",
            "    demand = [bid_qty[bid_px >= c].sum() for c in cands]",
            "    supply = [ask_qty[ask_px <= c].sum() for c in cands]",
            "    vol = np.minimum(demand, supply)",
            "    m = vol == vol.max()",
            "    imb = np.abs(np.subtract(demand, supply))",
            "    m &= imb == imb[m].min()",
            "    return cands[m].mean(), vol.max()",
        ], source="explainer/quant/house/funding.py", width=7.4).to_edge(UP, buff=0.4).shift(LEFT * 2.2)
        q = desk_question(r"A 2,000-share buy at any price: does it move the price more in the closing auction or "
                          r"in the continuous book?", r"in the book: in the auction it shifts the whole demand staircase and moves the "
                          r"crossing a little", width=5.4, font_size=21).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.6)
        with self.voiceover(
            "The House's version is nine lines: every order price is a candidate, demand and supply at each, the "
            "volume that clears, ties broken by imbalance. <bookmark mark='a'/> Run on the three hundred orders, it "
            f"prints {a['price']:.2f} and {a['volume']:,.0f} shares. And the question: does a two-thousand-share "
            "buy move the price more in the auction or in the book? <bookmark mark='z'/> In the book. In the auction it "
            "shifts the whole demand staircase and moves the crossing a little; in the book it walks up the ladder, as "
            "the numbers showed. That is why index funds trade the close. Books and auctions need a central venue. "
            "Most bonds, currencies and swaps have none."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab(self, card, ["call_auction(bp, bq, ap, aq)", f"({a['price']:.2f}, {a['volume']:,.0f})"])
            q.answer.set_opacity(0)
            self.play(FadeIn(q))
            vo.wait_until("z")
            self.play(q.answer.animate.set_opacity(1))
        self.wait(1.0)
        self.clear_scene()
