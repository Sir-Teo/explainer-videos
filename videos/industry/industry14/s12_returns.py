from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

ROWS = [("AWR", WATER), ("WTRG", WATER), ("AWK", WATER), ("RSG", RECYCLE), ("WM", RECYCLE), ("CLH", RECYCLE),
        ("XOM", BURN), ("NUE", BURN), ("DOW", BURN), ("MU", BAD), ("DAL", BAD), ("FCX", BAD)]


class Returns(VoiceoverScene):
    def construct(self):
        card(self, 10, "Why the steady money is bought", "Who wants a business that never surprises?",
             "Chapter ten. Why the steady money is bought.", lit=("moat", "dollar"))
        self.ranges()
        self.why()

    def ranges(self):
        M = R["returns"]["margins"]
        x0, x1 = -3.0, 6.2
        lo, hi = -0.9, 0.7

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)
        axis = VGroup(*[VGroup(DashedLine([X(v), 2.75, 0], [X(v), -3.0, 0], stroke_color=GREY_B if v else WHITE, stroke_width=1 if v else 2,
                                          stroke_opacity=0.4 if v else 0.7, dash_length=0.06),
                               tx(f"{100 * v:+.0f}%" if v else "0", 13, GREY_B).move_to([X(v), 3.0, 0])) for v in (-0.75, -0.5, -0.25, 0, 0.25, 0.5)])
        rows = VGroup()
        for i, (t, col) in enumerate(ROWS):
            y = 2.35 - 0.46 * i
            vals = list(M[t].values())
            seg = Line([X(min(vals)), y, 0], [X(max(vals)), y, 0], stroke_color=col, stroke_width=6, stroke_opacity=0.55)
            dots = VGroup(*[Dot([X(v), y, 0], radius=0.05, color=col) for v in vals])
            name = tx(NAMES[t], 15, col, bold=True).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            rows.add(VGroup(name, seg, dots))
        groups = VGroup(tx("water", 14, WATER, bold=True).move_to([-6.3, 2.35 - 0.46, 0]), tx("waste", 14, RECYCLE, bold=True).move_to([-6.3, 2.35 - 0.46 * 4, 0]),
                        tx("earlier parts", 14, BURN, bold=True).move_to([-6.3, 2.35 - 0.46 * 7.5, 0]))
        key = tx("each dot: one year's net income per dollar of revenue, 2010-2025", 14, GREY_A).to_edge(DOWN, buff=0.75)
        src = source("SEC EDGAR: Forms 10-K (net income, revenue), fiscal years 2010-2025 or as available", size=13)
        aw, rs, fx, da, mu = M["AWR"], M["RSG"], M["FCX"], M["DAL"], M["MU"]
        with self.voiceover(
            "Now the reason investors pay up for all this. Each row is a company; each dot, one year's profit per "
            "dollar of revenue since 2010. <bookmark mark='a'/> The water companies: tight clusters, every year well in "
            f"profit. American States Water never kept less than {100 * min(aw.values()):.0f} cents in the dollar or more "
            f"than {100 * max(aw.values()):.0f}. <bookmark mark='b'/> The waste companies: a little wider, still almost "
            f"always in profit; Republic between {100 * min(rs.values()):.0f} and {100 * max(rs.values()):.0f} cents. "
            "<bookmark mark='c'/> Now companies from earlier parts of this series. An oil major, a steelmaker, a "
            f"chemical company: wider. <bookmark mark='d'/> And a memory-chip maker, an airline and a copper miner: "
            f"from losses of {abs(100 * min(da.values())):.0f} and {abs(100 * min(fx.values())):.0f} cents in the dollar "
            f"to profits of {100 * max(mu.values()):.0f}. Same years, same economy. The difference is what the customer "
            "can do without."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(src), FadeIn(key), *[FadeIn(r_[0]) for r_ in rows])
            for m_, sl in zip("abcd", (slice(0, 3), slice(3, 6), slice(6, 9), slice(9, 12))):
                vo.wait_until(m_)
                self.play(*[AnimationGroup(Create(r_[1]), LaggedStart(*[FadeIn(d, scale=0.5) for d in r_[2]], lag_ratio=0.05)) for r_ in rows[sl]],
                          FadeIn(groups[{"a": 0, "b": 1, "c": 2, "d": 2}[m_]]) if m_ in "abc" else Wait(0.01), run_time=2.0)
        self.clear_scene()

    def why(self):
        G = R["regulated"]
        items = [(draw.coin_stack(5, 0.18) if hasattr(draw, "coin_stack") else draw.coin(0.3), "Prices that follow costs",
                  "contracts that rise with the CPI and fuel; regulators who set returns after inflation"),
                 (draw.landfill_section(1.2, 0.5, fill=1.0), "Assets nobody can copy",
                  "a permitted landfill, a city's pipes: decades to replace, if anyone is allowed to"),
                 (draw.water_tower(0.9), "Owners who want exactly that",
                  "pension, sovereign wealth and infrastructure funds: 'long-term, low-risk and low-return'")]
        rows = VGroup()
        for i, (ic, h, d) in enumerate(items):
            ic.scale_to_fit_height(min(ic.height, 0.75))
            if ic.width > 1.2:
                ic.scale_to_fit_width(1.2)
            y = 1.7 - 1.35 * i
            ic.move_to([-5.2, y, 0])
            t = VGroup(tx(h, 22, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-4.2, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(ic, t))
        rcv = tx(f"England and Wales: £{get('iwc.rcv'):.0f}bn of regulated water assets (2024/25)", 17, UK, bold=True).to_edge(DOWN, buff=1.1)
        warn = tx("the catch: borrow too much against it, and the steadiness belongs to the lenders", 16, BAD).to_edge(DOWN, buff=0.7)
        src = source("Waste Management, Form 10-K 2025; Independent Water Commission, Final Report (July 2025)", size=13)
        with self.voiceover(
            "Three things make these businesses steady, and all three are what a certain kind of owner is looking for. "
            "<bookmark mark='a'/> Prices that follow costs: Waste Management's contracts carry yearly price changes linked "
            "to the consumer price index and fuel, and England's regulator sets its returns after inflation. "
            "<bookmark mark='b'/> Assets nobody can copy: a permitted landfill, or a city's pipes, which would take "
            "decades to replace even if anyone were allowed to. <bookmark mark='c'/> And owners who want exactly that. "
            "Britain's Water Commission said the industry should attract investors with a 'long-term, low-risk and "
            "low-return' approach: pension funds, sovereign wealth funds, infrastructure funds. <bookmark mark='d'/> In "
            f"England and Wales alone, the regulated water assets are worth about £{get('iwc.rcv'):.0f} billion. "
            "<bookmark mark='e'/> The catch is the one Thames Water showed: borrow too much against a steady business, "
            "and the steadiness belongs to the lenders."
        ) as vo:
            head = tx("Why these businesses are steady", 24, WHITE, bold=True).to_edge(UP, buff=0.4)
            self.play(FadeIn(src), FadeIn(head), *[FadeIn(r_[0].copy().set_opacity(0.2)) for r_ in rows])
            for m_, r_ in zip("abc", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_[0], scale=0.8), FadeIn(r_[1], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(rcv, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(warn, shift=UP * 0.1))
        self.clear_scene()
