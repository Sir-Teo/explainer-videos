from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, FAST_C, GOOD, HURDLE, INV_C, PART, SNIPE_C, SPREAD_C, fit_right, load)


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
        with self.voiceover(f"Chapter two, answering the pause. The slow rule has a one-minute signed mark of {d['mk60']:.1f} ticks per fill. Its separate final-mid profit mean is {d['pnl_per_fill']:.1f}. Both omit fees and executable liquidation. We will keep the horizon and fill-selection rules visible."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def design(self):
        rows = [cmath(r"\text{quote}", r":", r"\text{join the best bid and offer, at the back}", font_size=34),
                cmath(r"\text{reprice}", r":", r"\text{cancel and rejoin when the best moves away}", font_size=34),
                cmath(r"|I|", r"\le", r"5\ \text{units}", font_size=40, colors={r"|I|": INV_C}),
                cmath(r"\text{fills}", r":", r"\text{coarse-grid queue reconstruction assumptions}", font_size=34)]
        whys = [why(r"one unit per side, with its own market impact excluded by assumption"),
                why(r"checked every 100 ms on the best-quote grid: a chosen coarse resolution, not a lower bound on actual reaction speed"),
                why(r"an inventory limit: at five units long it stops bidding, at five short it stops offering"),
                why(r"trades eat the queue from the front, cancellations pro rata, and any trade through the price fills")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The simulated maker. <bookmark mark='a'/> It posts one unit behind displayed quantity while assuming its own orders do not change prices. <bookmark mark='b'/> It reconstructs events on a hundred-millisecond grid, canceling or retaining old levels under the source's priority rules. <bookmark mark='c'/> Inventory is limited to five units each way. <bookmark mark='d'/> At-price volume must exceed the queue ahead; cancellations are allocated pro rata and trades through the price fill. These are reconstruction assumptions, not message-level queue observations."
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
                                                                         r"in its 100 ms", r"after 1 min", r"final-mid per fill")])
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
        foot = wrapped_label(r"17 May 2023, BTCUSDT perpetual; in ticks of \$0.10 per fill; fast: an omniscient within-step rule that "
                             r"cancels before any sweep; filtered: it also withdraws a side when the queue imbalance warns "
                             r"(Part 36)", 12.0, 15, GREY_A).to_edge(DOWN, buff=0.5)
        s, f, ff = d["slow"], d["fast"], d["fast, filtered"]
        with self.voiceover(
            f"On the seventeenth of May. <bookmark mark='a'/> The slow rule has {s['n']:,} fills, roughly half a tick of pre-step execution edge, an average same-step mid move of {s['step']:.1f}, and final-mid profit of {s['pnl_per_fill']:.1f} ticks per fill. The separate one-minute column is {s['mk60']:.1f}. <bookmark mark='b'/> The fast variant knows all trades in the step before deciding whether a through-price fill survives, and has final-mid profit {f['pnl_per_fill']:.1f}. <bookmark mark='c'/> Adding the imbalance rule gives {ff['pnl_per_fill']:.1f}. The variants select different fills and inventory paths, so this is not an identified causal speed effect."
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
            "A decomposition of the slow rule's signed one-minute mark. <bookmark mark='a'/> Pre-step execution edge, then the same-step mid move, then increments to the one-second, ten-second and one-minute marks. Those components telescope to the one-minute statistic; the half-spread is already included. <bookmark mark='b'/> The same-step increment is the largest single negative piece here, but later movement matters too. A grid cannot recover exact ordering or an actual cancel latency within that step."
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
            "Signed marks for three different selected fill sets. <bookmark mark='a'/> The first point uses the previous grid mid, the next includes the fill step, followed by one, ten and sixty grid-second marks. Near the day end, horizons are clipped. <bookmark mark='b'/> All three minute means are negative, with the filtered set least negative. This documents conditional marks under the reconstruction. It does not separate causal speed, predictive skill or market impact."
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
                why(r"the retained selected set has a less negative one-second signed mark"),
                why(r"counts and means both change; a product decomposition depends on the reference mean, and this is not a causal forecast estimate or proof of "
                    r"earning the spread")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What the imbalance filter changes. <bookmark mark='a'/> It removes nearly two-thirds of the hindsight variant's selected fills. <bookmark mark='b'/> The retained set has a less negative one-second signed mark. <bookmark mark='c'/> The final-mid total loss also falls, with both a lower count and a changed mean. A product decomposition depends on the chosen reference mean; these selected comparisons do not by themselves identify a causal forecast benefit."
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
        self.add(cards[0])
        with self.voiceover(
            "Possible mechanisms, not identified counterparties. <bookmark mark='a'/> Cross-venue information can make a quote stale. <bookmark mark='b'/> Liquidations can generate one-sided aggressive flow. <bookmark mark='c'/> Other makers may withdraw ahead of a move. Our single-venue aggregate tape does not identify these trader types or attribute each replay loss to them."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
                cmath(r"\text{selected replay gap}", r"\approx", rf"{gap:.0f}\ \text{{ticks a fill}}", font_size=38,
                      colors={r"\text{selected replay gap}": HURDLE})]
        whys = [why(r"the slow maker is filled by every sweep that passes through its price before it can cancel"),
                why(r"the idealised fast maker escapes all of them, and is filled only by trades that stop at its price"),
                why(r"the variants select different fills and inventory paths; this difference is not causal or a universal speed bound")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"Compare the replay variants. <bookmark mark='a'/> The slow rule accepts through-price fills. <bookmark mark='b'/> The idealized fast rule discards them with within-step hindsight. <bookmark mark='c'/> Their final-mid means differ by about {gap:.0f} ticks per selected fill. Different denominators and inventory paths prevent interpreting this as the causal value of a latency improvement or a universal upper bound."
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
                cmath(r"\text{the maker}", r":", r"\text{large inventory variation under the limit}", font_size=36,
                      colors={r"\text{the maker}": BAD})]
        whys = [why(r"the replay's only inventory control"),
                why(r"a descriptive grid-path standard deviation; it does not measure boundary occupancy or identify informed flow"),
                why(r"at a limit the rule stops one side; standard deviation alone does not measure time spent at a limit. A model "
                    r"skew changes posting earlier, but its performance is not tested here")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"The inventory statistic. <bookmark mark='a'/> A hard five-unit limit is the rule's only explicit inventory control. <bookmark mark='b'/> Inventory standard deviation is {d['slow']['inv_sd']:.1f} units over the grid path. <bookmark mark='c'/> At a boundary it stops posting one side. Standard deviation does not report boundary occupancy or prove what causes it. GLFT supplies an alternative control model, whose performance this replay has not evaluated."
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
        head = VGroup(label(r"final-mid per fill, ticks", font_size=16, color=GREY_B),
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
                why(r"a constant rebate of that size offsets this gross final-mid replay loss arithmetically; this omits "
                    r"funding, liquidation, hedging, latency and impact, so it is not a complete business break-even estimate")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"Converting the illustrative final-mid loss. <bookmark mark='a'/> One ten-cent tick is {tb:.3f} basis points at the day's representative price. <bookmark mark='b'/> The filtered rule's mean loss is {need:.2f} basis points per fill under this conversion. <bookmark mark='c'/> A constant rebate of that size would offset this chosen gross replay loss arithmetically. It is not a complete break-even estimate: hedging, liquidation, funding, latency and market impact are absent."
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
            desk_question(r"queue position", r"queue position is reconstructed; Part 36 "
                          r"compares different conditional fill sets, without identifying a causal priority value", width=12.4, font_size=19),
            desk_question(r"hedging and other venues", r"inventory hedged on another exchange or in spot turns the "
                          r"inventory P\&L into a basis trade; none of that is in a single-book replay", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What the replay leaves out", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "What remains unmeasured. <bookmark mark='a'/> The fast rule uses within-step hindsight; the data cannot certify real cancel speed or order precedence inside one hundred milliseconds. <bookmark mark='b'/> Queue position is reconstructed. Part thirty-six's front and back results compare different selected fill sets and are not causal priority prices. <bookmark mark='c'/> Cross-venue hedging, fees, funding and executable inventory liquidation are missing. The conclusion is limited to these specified replay rules."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label("Avellaneda and Stoikov assume quotes at distance $\\delta$ fill at rate $A e^{-k\\delta}$. Fitted to Bitcoin's tape, how far from the mid would their optimal quotes sit: one tick, five, or thirty?", 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. Avellaneda and Stoikov's model assumes quotes fill at a rate that decays exponentially "
            "with their distance from the mid. Fitted to Bitcoin's tape, how far away would its optimal quotes sit: one "
            "tick, five, or thirty?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
