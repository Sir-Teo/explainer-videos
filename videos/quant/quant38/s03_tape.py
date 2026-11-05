from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, FAST_C, GOOD, HURDLE, INV_C, PART, SNIPE_C, SPREAD_C, load)


class Tape(VoiceoverScene):
    def construct(self):
        mk = load("maker")
        self.card(mk)
        self.design()
        self.table(mk)
        self.waterfall(mk)
        self.markout_curve(mk)
        self.filter_effect(mk)
        self.who_hits()
        self.slow_cost(mk)
        self.inventory(mk)
        self.by_day(mk)
        self.fees(mk)
        self.what_missing()
        self.question()

    def card(self, mk):
        d = mk["days"]["2023-05-17"]["slow"]
        c = chapter_card(2, r"A maker on the tape", r"What happens to a simple quoting rule on Bitcoin's real order flow?",
                         part=PART)
        with self.voiceover("Chapter two, and the answer to the pause: a loss of about "
                            f"{abs(d['pnl_per_fill']):.0f} ticks per fill. The half tick of spread is real, but each fill "
                            "is followed by a move against the maker forty times larger. This chapter shows where it goes."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def design(self):
        rows = [cmath(r"\text{quote}", r":", r"\text{join the best bid and offer, at the back}", font_size=34),
                cmath(r"\text{reprice}", r":", r"\text{cancel and rejoin when the best moves away}", font_size=34),
                cmath(r"|I|", r"\le", r"5\ \text{units}", font_size=40, colors={r"|I|": INV_C}),
                cmath(r"\text{fills}", r":", r"\text{Part 36's queue replay on the real tape}", font_size=34)]
        whys = [why(r"a tiny order on each side, so the maker never moves the market itself"),
                why(r"checked every 100 ms on the best-quote grid: the slowest reaction a maker could have"),
                why(r"an inventory limit: at five units long it stops bidding, at five short it stops offering"),
                why(r"trades eat the queue from the front, cancellations pro rata, and any trade through the price fills")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The maker. <bookmark mark='a'/> It joins the best bid and the best offer, at the back of each queue, with a "
            "tiny size. <bookmark mark='b'/> Every tenth of a second it checks the book, and when the best price has "
            "moved away it cancels and rejoins. <bookmark mark='c'/> It holds at most five units either way. "
            "<bookmark mark='d'/> And its fills come from Part thirty-six's replay of the real queue against the real "
            "trades."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def table(self, mk):
        d = mk["days"]["2023-05-17"]
        hx = [-4.8, -2.6, -0.8, 1.0, 2.8, 4.8]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"maker", r"fills a day", r"half-spread",
                                                                         r"in its 100 ms", r"after 1 min", r"P\&L per fill")])
        tab = VGroup(head)
        cols = {"slow": SNIPE_C, "fast": FAST_C, "fast, filtered": GOOD}
        for name in ("slow", "fast", "fast, filtered"):
            r = d[name]
            tab.add(VGroup(label(name, font_size=18, color=cols[name]), MathTex(f"{r['n']:,}".replace(",", "{,}"),
                                                                                  font_size=24),
                           MathTex(f"{r['half']:+.2f}", font_size=24, color=SPREAD_C),
                           MathTex(f"{r['step']:+.1f}", font_size=24), MathTex(f"{r['mk60']:+.1f}", font_size=24),
                           MathTex(f"{r['pnl_per_fill']:+.1f}", font_size=24, color=cols[name])))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.9 * j, 0])
        foot = wrapped_label(r"17 May 2023, BTCUSDT perpetual; in ticks of \$0.10 per fill; fast: an idealised maker that "
                             r"cancels before any sweep; filtered: it also withdraws a side when the queue imbalance warns "
                             r"(Part 36)", 12.0, 15, GREY_A).to_edge(DOWN, buff=0.5)
        s, f, ff = d["slow"], d["fast"], d["fast, filtered"]
        with self.voiceover(
            "The result for a whole day, the seventeenth of May. <bookmark mark='a'/> The slow maker is filled "
            f"{s['n']:,} times. It earns half a tick each time, then loses about {abs(s['step']):.0f} ticks within the "
            f"same tenth of a second, and {abs(s['pnl_per_fill']):.0f} ticks per fill in all. <bookmark mark='b'/> An "
            "idealised fast maker, which cancels before any sweep reaches it, is filled half as often and loses "
            f"{abs(f['pnl_per_fill']):.0f}. <bookmark mark='c'/> Add Part thirty-six's imbalance warning, withdrawing "
            f"the threatened side, and the loss falls to {abs(ff['pnl_per_fill']):.1f} ticks a fill. Still a loss."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def waterfall(self, mk):
        d = mk["days"]["2023-05-17"]["slow"]
        steps_ = [("half-spread", d["half"], SPREAD_C), ("its 100 ms", d["step"], SNIPE_C),
                  ("to 1 s", d["mk1"] - d["step"] - d["half"], SNIPE_C), ("to 10 s", d["mk10"] - d["mk1"], SNIPE_C),
                  ("to 1 min", d["mk60"] - d["mk10"], SNIPE_C)]
        lo = float(np.floor(min(0, d["mk60"]) / 5) * 5) - 5
        g = axes([-0.5, len(steps_) + 0.5], [lo, 5], x_length=8.8, y_length=4.4, xlabel=r"", ylabel=r"ticks per fill",
                 xticks=[], yticks=[lo, 0], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        labs = VGroup()
        level = 0.0
        for i, (name, v, col) in enumerate(steps_):
            a, b_ = level, level + v
            rect = Rectangle(width=0.9, height=max(1e-3, abs(ax.c2p(0, b_)[1] - ax.c2p(0, a)[1])),
                             fill_color=col if v < 0 else SPREAD_C, fill_opacity=0.85, stroke_width=0)
            rect.move_to(ax.c2p(i, (a + b_) / 2))
            bars.add(rect)
            labs.add(label(name, font_size=15, color=GREY_A).next_to(ax.c2p(i, max(a, b_)), UP, buff=0.12))
            level = b_
        total = label(rf"after a minute: {d['mk60']:+.1f} ticks a fill", font_size=20, color=BAD).to_edge(UP, buff=0.7)
        with self.voiceover(
            "Where the money goes, per fill. <bookmark mark='a'/> Half a tick earned. Then the mid moves against the "
            "maker in the very tenth of a second of the fill, by far the largest piece, then more over the next second, "
            "the next ten, and the minute after. <bookmark mark='b'/> Most of the loss is decided before a maker that "
            "looks only every tenth of a second can react."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.4), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(total))
        self.wait(0.4)
        self.clear_scene()

    def markout_curve(self, mk):
        d = mk["days"]["2023-05-17"]
        cols = {"slow": SNIPE_C, "fast": FAST_C, "fast, filtered": GOOD}
        xs = [0, 1, 2, 3, 4]
        labels_ = [r"at fill", r"0.1 s", r"1 s", r"10 s", r"1 min"]
        lo = float(np.floor(min(d[n]["mk60"] for n in cols) / 5) * 5) - 5
        g = axes([-0.3, 4.3], [lo, 2], x_length=8.0, y_length=4.2, xlabel=r"", ylabel=r"markout per fill, ticks",
                 xticks=[], yticks=[lo, 0], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        curves = VGroup()
        for n, col in cols.items():
            r = d[n]
            ys = [r["half"], r["half"] + r["step"], r["mk1"], r["mk10"], r["mk60"]]
            curves.add(VGroup(curve(ax, xs, ys, col, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.06, color=col)
                                                                         for a, b in zip(xs, ys)]))
        ticks = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(x, lo), DOWN, buff=0.15)
                         for x, t in zip(xs, labels_)])
        leg = legend([(c, n) for n, c in cols.items()], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "The markout over time, for the three makers. <bookmark mark='a'/> All start at plus half a tick. The slow "
            "maker drops at once, inside the tenth of a second of its fills; the fast ones drop more slowly, over the "
            "following seconds. <bookmark mark='b'/> After a minute, all three are below zero, the filtered one least. "
            "Speed decides how much of the move happens before you can react; a forecast decides how much of the flow "
            "you accept at all."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ticks), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(curves[0]), Create(curves[1]))
            vo.wait_until("b")
            self.play(Create(curves[2]))
        self.wait(0.4)
        self.clear_scene()

    def filter_effect(self, mk):
        d = mk["days"]["2023-05-17"]
        f, ff = d["fast"], d["fast, filtered"]
        rows = [cmath(r"\text{fills}", r":", rf"{f['n']:,} \to {ff['n']:,}".replace(",", "{,}"), font_size=38),
                cmath(r"\text{markout at 1 s}", r":", rf"{f['mk1']:+.1f} \to {ff['mk1']:+.1f}", font_size=38),
                cmath(r"\text{total}", r":", rf"{f['n'] * f['pnl_per_fill']:,.0f} \to {ff['n'] * ff['pnl_per_fill']:,.0f}\ "
                      r"\text{ticks}".replace(",", "{,}"), font_size=36, colors={r"\text{total}": GOOD})]
        whys = [why(r"withdrawing the side the queue imbalance threatens removes almost two-thirds of the fills"),
                why(r"the fills it keeps are less toxic in the first second"),
                why(r"the day's loss shrinks most from trading less; a filter is a way of declining the worst flow, not of "
                    r"earning the spread")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What the filter does. <bookmark mark='a'/> Withdrawing the side the imbalance threatens removes almost "
            "two-thirds of the fast maker's fills. <bookmark mark='b'/> The fills it keeps lose less in the first second. "
            "<bookmark mark='c'/> The day's total loss shrinks mostly because it trades less. A filter is a way of "
            "declining the worst flow, not of earning the spread."
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

    def who_hits(self):
        cards = VGroup(
            desk_question(r"other venues first", r"Bitcoin's price is discovered across many exchanges and in spot; a quote "
                          r"here is stale the moment another venue moves (Part 35's price discovery)", width=12.4,
                          font_size=19),
            desk_question(r"forced flow", r"liquidations of leveraged positions arrive as market orders in bursts, and "
                          r"sweep the book in one direction (Part 35, Part 39)", width=12.4, font_size=19),
            desk_question(r"faster makers' cancels", r"when better-informed makers withdraw first, the quotes left at the "
                          r"touch are the slow ones, and the sweep finds them", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Who is on the other side of those fills? <bookmark mark='a'/> Traders reacting to other venues: Bitcoin's "
            "price is discovered across many exchanges and in spot, and a quote here is stale the moment another venue "
            "moves. <bookmark mark='b'/> Forced flow: liquidations of leveraged positions arrive as bursts of market "
            "orders in one direction. <bookmark mark='c'/> And faster makers withdraw first, so the quotes left at the "
            "touch when the sweep arrives are the slow ones."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def slow_cost(self, mk):
        d = mk["days"]["2023-05-17"]
        gap = d["fast"]["pnl_per_fill"] - d["slow"]["pnl_per_fill"]
        rows = [cmath(r"\text{slow}", r":", rf"{d['slow']['pnl_per_fill']:+.1f}\ \text{{ticks}}", font_size=40,
                      colors={r"\text{slow}": SNIPE_C}),
                cmath(r"\text{fast}", r":", rf"{d['fast']['pnl_per_fill']:+.1f}\ \text{{ticks}}", font_size=40,
                      colors={r"\text{fast}": FAST_C}),
                cmath(r"\text{the value of speed}", r"\approx", rf"{gap:.0f}\ \text{{ticks a fill}}", font_size=38,
                      colors={r"\text{the value of speed}": HURDLE})]
        whys = [why(r"the slow maker is filled by every sweep that passes through its price before it can cancel"),
                why(r"the idealised fast maker escapes all of them, and is filled only by trades that stop at its price"),
                why(r"the difference is what the race is about: being able to withdraw before the price runs through you")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The price of slowness. <bookmark mark='a'/> The slow maker is filled by every sweep that runs through its "
            "price. <bookmark mark='b'/> The idealised fast one escapes them, and is filled only by trades that stop at "
            f"its price. <bookmark mark='c'/> The difference, about {gap:.0f} ticks a fill, is what the speed race is "
            "about: the ability to withdraw before the price runs through you. Chapter six puts this into a model."
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

    def inventory(self, mk):
        d = mk["days"]["2023-05-17"]
        rows = [cmath(r"\text{limit}", r":", r"\pm 5\ \text{units}", font_size=38),
                cmath(r"\text{sd of inventory}", r"\approx", rf"{d['slow']['inv_sd']:.1f}\ \text{{units}}", font_size=38,
                      colors={r"\text{sd of inventory}": INV_C}),
                cmath(r"\text{the maker}", r":", r"\text{usually near a limit, one-sided}", font_size=36,
                      colors={r"\text{the maker}": BAD})]
        whys = [why(r"the replay's only inventory control"),
                why(r"close to the limit itself: fills are not balanced; sweeps fill one side again and again"),
                why(r"a maker pinned at its limit quotes only one side, which is exactly when the flow is one-sided: GLFT's "
                    r"skew would lean earlier and harder")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And its inventory. <bookmark mark='a'/> The only control is a limit of five units each way. "
            f"<bookmark mark='b'/> The inventory's standard deviation is {d['slow']['inv_sd']:.1f} units, close to the limit "
            "itself: sweeps fill the same side again and again. <bookmark mark='c'/> So the maker spends much of the day "
            "pinned at a limit, quoting one side, exactly when the flow is one-sided. GLFT's skew would lean earlier and "
            "harder."
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

    def by_day(self, mk):
        days = list(mk["days"].keys())
        hx = [-4.0, -1.2, 1.6, 4.4]
        head = VGroup(label(r"P\&L per fill, ticks", font_size=16, color=GREY_B),
                      *[label(d[5:], font_size=16, color=GREY_B if d != "2023-05-20" else HURDLE) for d in days])
        tab = VGroup(head)
        for name, col in (("slow", SNIPE_C), ("fast", FAST_C), ("fast, filtered", GOOD)):
            tab.add(VGroup(label(name, font_size=18, color=col),
                           *[MathTex(f"{mk['days'][d][name]['pnl_per_fill']:+.1f}", font_size=26) for d in days]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        foot = wrapped_label(r"two weekdays and a Saturday", 10.0, 16, GREY_A).to_edge(DOWN, buff=0.8)
        best = max(mk["days"][d]["fast, filtered"]["pnl_per_fill"] for d in days)
        with self.voiceover(
            "On three days, two weekdays and a Saturday. <bookmark mark='a'/> The ordering never changes: slow worst, "
            f"fast better, fast and filtered best, but never positive; the best day is {best:.1f} ticks a fill. A "
            "quoting rule with no forecast of its own, at the touch, on this market, pays its counterparties."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def fees(self, mk):
        tb = mk["tick_bp"]
        ff = mk["days"]["2023-05-17"]["fast, filtered"]["pnl_per_fill"]
        need = abs(ff) * tb
        rows = [cmath(r"1\ \text{tick}", r"=", rf"{tb:.3f}\ \text{{bp}}", font_size=40),
                cmath(r"\text{loss per fill}", r"=", rf"{abs(ff):.1f}\ \text{{ticks}} = {need:.2f}\ \text{{bp}}", font_size=36,
                      colors={r"\text{loss per fill}": BAD}),
                cmath(r"\text{rebate needed}", r"\approx", rf"{need:.2f}\ \text{{bp of the notional}}", font_size=36,
                      colors={r"\text{rebate needed}": HURDLE})]
        whys = [why(r"at \$27{,}000, the \$0.10 tick is a tiny fraction of the price"),
                why(r"the best rule's loss on 17 May, converted"),
                why(r"a maker rebate of that size would just break even; standard maker fees go the other way, so only the "
                    r"lowest fee tiers, speed and better forecasts make this business possible")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "In basis points. <bookmark mark='a'/> A tick is "
            f"{tb:.3f} of a basis point. <bookmark mark='b'/> So the best rule's loss is about {need:.2f} basis points a "
            "fill. <bookmark mark='c'/> A rebate of that size on each fill would just break even. Standard maker fees go "
            "the other way, so the business exists only for firms with the lowest fee tiers, real speed, and better "
            "forecasts than ours."
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

    def what_missing(self):
        cards = VGroup(
            desk_question(r"real speed", r"real makers react in microseconds, not a tenth of a second; our fast maker "
                          r"is an idealisation, but the replay cannot see inside 100 ms", width=12.4, font_size=19),
            desk_question(r"queue position", r"a maker that rests early at a level sits near the front, where Part 36 "
                          r"found fills far less toxic than at the back", width=12.4, font_size=19),
            desk_question(r"hedging and other venues", r"inventory hedged on another exchange or in spot turns the "
                          r"inventory P\&L into a basis trade; none of that is in a single-book replay", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the replay leaves out, so the conclusion is not overstated. <bookmark mark='a'/> Real makers react in "
            "microseconds; our fast maker is an idealisation, and the replay cannot see inside a tenth of a second. "
            "<bookmark mark='b'/> Real makers hold places near the front of queues, where Part thirty-six found fills "
            "far less toxic. <bookmark mark='c'/> And they hedge on other venues. The lesson stands: the spread itself "
            "pays for almost nothing."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"Avellaneda and Stoikov assume quotes at distance $\delta$ fill at rate $A e^{-k\delta}$. Fitted to "
                       r"Bitcoin's tape, how far from the mid would their optimal quotes sit: one tick, five, or thirty?")
        with self.voiceover(
            "Pause and predict. Avellaneda and Stoikov's model assumes quotes fill at a rate that decays exponentially "
            "with their distance from the mid. Fitted to Bitcoin's tape, how far away would its optimal quotes sit: one "
            "tick, five, or thirty?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
