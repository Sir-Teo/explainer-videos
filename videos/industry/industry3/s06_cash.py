from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403


def bridge(steps, scale, x0=-6.0, dx=1.5, base=-1.6, w=1.05, size=14):
    """A horizontal waterfall: [(label, amount, kind, colour)], kind 'total' or 'step'."""
    bars, labs, vals = VGroup(), VGroup(), VGroup()
    level = 0.0
    for k, (lab, v, kind, col) in enumerate(steps):
        x = x0 + k * dx
        if kind == "total":
            lo, hi = min(0.0, v), max(0.0, v)
            level = v
        else:
            lo, hi = sorted((level, level + v))
            level += v
        r = Rectangle(width=w, height=max((hi - lo) * scale, 0.02), fill_color=col, fill_opacity=0.9,
                      stroke_width=0).move_to(np.array([x, base + (lo + hi) / 2 * scale, 0]))
        bars.add(r)
        t = VGroup(*[T(p, size, I.TEXT) for p in lab.split("\n")]).arrange(DOWN, buff=0.03)
        labs.add(t.move_to(np.array([x, base - 2.35, 0])))
        sign = "+" if (kind == "step" and v > 0) else ("-" if v < 0 else "")
        vals.add(TB(f"{sign}${abs(v):,.0f}", size + 1, col).next_to(r, UP if v >= 0 or kind == "total" else DOWN,
                                                                     buff=0.05))
    return bars, labs, vals


class Cash(VoiceoverScene):
    def construct(self):
        card(self, 5, "Profit is not cash", "How can a profitable business run out of money?",
             "Chapter five. Profit is not cash.", lit=("dollar", "change"))
        self.bakery()
        self.growing()
        self.giants()

    def bakery(self):
        y = R["bakery_year"]
        i, b, c = y["income"], y["balance"], y["cash"]
        G, Rd, Bl = I.PROFIT, I.COST, "#7EC8F5"
        steps = [("Net\nprofit", i["net"], "total", G), ("Oven's wear:\nno cash spent", i["depreciation"], "step", G),
                 ("Cafes have\nnot paid", -b["receivables"], "step", Rd), ("Flour in\nstock", -b["inventory"], "step", Rd),
                 ("Miller not\nyet paid", b["payables"], "step", G), ("Cash from\nthe business", c["operating"], "total", Bl),
                 ("The oven", -45_000, "step", Rd), ("Free\ncash", c["free"], "total", Rd)]
        bars, labs, vals = bridge(steps, scale=2.2 / 45_000, x0=-5.6, dx=1.6, base=0.9)
        axis = Line(np.array([-6.5, 0.9, 0]), np.array([6.5, 0.9, 0]), color=I.EDGE)
        head = T("The bakery's first year: from profit to cash", 24, I.TEXT).to_edge(UP, buff=0.35)
        src = estimate_tag("illustrative: the model bakery", corner=DR)
        with self.voiceover(
            f"The bakery made {say_usd(i['net'])} of profit. How much cash did it make? <bookmark mark='a'/> Start "
            "from the profit. <bookmark mark='b'/> Add back the oven's wear: it was a cost, but no money left the "
            f"till for it this year. <bookmark mark='c'/> Take off the {say_usd(b['receivables'])} the cafes still "
            "owe: sales counted, cash not received. Take off the flour sitting in the store room. <bookmark "
            "mark='d'/> Add the miller's bill, not yet paid. <bookmark mark='e'/> The business itself brought in "
            f"{say_usd(c['operating'])} of cash, less than its profit. <bookmark mark='f'/> And the oven cost forty-"
            f"five thousand in cash this year, so over the year the bakery's own operations used up "
            f"{say_usd(-c['free'])} more than they produced. The owner's savings and the bank paid for the "
            "difference. That is why accounts come with a third statement, the cash-flow statement: profit is an "
            "opinion about the year, cash is a fact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            marks = {"a": [0], "b": [1], "c": [2, 3], "d": [4], "e": [5], "f": [6, 7]}
            for m, idx in marks.items():
                vo.wait_until(m)
                self.play(*[AnimationGroup(FadeIn(bars[j], shift=UP * 0.05), FadeIn(labs[j]), FadeIn(vals[j]))
                            for j in idx], run_time=0.9)
        self.clear_scene()

    def growing(self):
        G = R["growth"]
        mx = max(max(abs(g["profit"]), abs(g["cash"])) for g in G)
        pa = viz.plot_axes((0.5, 5.5), (-350_000, 100_000), x_length=8.0, y_length=4.4, xticks=[1, 2, 3, 4, 5],
                           yticks=[-300_000, -200_000, -100_000, 0, 100_000], xfmt=lambda v: f"year {v:.0f}",
                           yfmt=lambda v: f"${v / 1e3:,.0f}k", size=15).shift(LEFT * 1.6 + DOWN * 0.4)
        zero = DashedLine(pa.ax.c2p(0.5, 0), pa.ax.c2p(5.5, 0), color=I.FAINT, stroke_width=1.5)
        prof = VMobject(stroke_color=I.PROFIT, stroke_width=4).set_points_as_corners(
            [pa.ax.c2p(k + 1, g["profit"]) for k, g in enumerate(G)])
        cash = VMobject(stroke_color=I.COST, stroke_width=4).set_points_as_corners(
            [pa.ax.c2p(k + 1, g["cash"]) for k, g in enumerate(G)])
        pdots = VGroup(*[Dot(pa.ax.c2p(k + 1, g["profit"]), color=I.PROFIT, radius=0.06) for k, g in enumerate(G)])
        cdots = VGroup(*[Dot(pa.ax.c2p(k + 1, g["cash"]), color=I.COST, radius=0.06) for k, g in enumerate(G)])
        lp = TB("profit each year", 20, I.PROFIT).next_to(pa.ax.c2p(5, G[-1]["profit"]), UP, buff=0.15)
        lc = TB("cash in the bank", 20, I.COST).next_to(pa.ax.c2p(5, G[-1]["cash"]), UP, buff=0.15).shift(LEFT * 0.6)
        side = VGroup(T("Sales up 60% a year", 18, I.TEXT), T("a new shop and oven each year", 18, I.TEXT),
                      T("cafes given 60 days to pay", 18, I.TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(
            UR, buff=0.5).shift(DOWN * 0.6)
        head = T("The same bakery, growing fast", 24, I.TEXT).to_corner(UL, buff=0.4)
        src = estimate_tag("illustrative: explainer/industry/works/firm.py", corner=DR)
        with self.voiceover(
            "Now let the bakery grow. <bookmark mark='a'/> It opens a new shop and buys a new oven every year, sales "
            "rise sixty percent a year, and to win the cafes it gives them sixty days to pay instead of twenty. "
            f"<bookmark mark='b'/> Its profit rises every year, from {say_usd(G[0]['profit'])} to "
            f"{say_usd(G[-1]['profit'])}. <bookmark mark='c'/> And its cash runs out in the second year. Every "
            "extra sale ties up more money in what the cafes owe and in stock, and every new shop needs an oven "
            "paid for up front. <bookmark mark='d'/> Many small businesses fail this way: profitable on paper "
            "and out of cash. The cure is not more profit; it is more patient money, from the owner, "
            "the bank or investors, or slower growth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(side, shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(Create(prof), FadeIn(pdots), FadeIn(lp), run_time=2)
            vo.wait_until("c")
            self.play(Create(cash), FadeIn(cdots), FadeIn(lc), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(cdots[1], color=I.COST, scale_factor=1.6))
        self.clear_scene()
        del mx

    def giants(self):
        M, N = R["cash"]["msft"], R["cash"]["nee"]
        steps = [("Net\nincome", M["ni"], "total", I.PROFIT), ("Cash from\noperations", M["ocf"], "total", "#7EC8F5"),
                 ("Data centres\nand equipment", -M["capex"], "step", I.COST), ("Free\ncash", M["fcf"], "total", I.MONEY)]
        bars, labs, vals = bridge(steps, scale=3.6 / 190, x0=-5.4, dx=1.55, base=-1.0, size=14)
        for l in labs:  # noqa: E741
            l.shift(UP * 1.1)
        h1 = TB("Microsoft, fiscal 2026 ($bn)", 21, CO["msft"]).move_to(np.array([-3.1, 3.2, 0]))
        q = VGroup(T("First quarter of fiscal 2027:", 17, I.DIM),
                   T(f"free cash {bn(M['q1']['fcf'])}, against {bn(M['q1_prev']['fcf'])} a year before", 17, I.TEXT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(np.array([-3.1, -2.9, 0]))
        steps2 = [("Cash from\noperations", N["ocf"], "total", "#7EC8F5"),
                  ("New plants\nand wires", -N["capex"], "step", I.COST), ("Free\ncash", N["fcf"], "total", I.COST)]
        bars2, labs2, vals2 = bridge(steps2, scale=3.6 / 190 * 3, x0=2.6, dx=1.55, base=-1.0, size=14)
        for l in labs2:  # noqa: E741
            l.shift(UP * 1.1)
        h2 = TB("NextEra, 2025 ($bn)", 21, CO["nee"]).move_to(np.array([4.15, 3.2, 0]))
        n2 = T("scale x3; the gap is borrowed", 15, I.DIM).move_to(np.array([4.15, -2.9, 0]))
        axis = VGroup(Line(np.array([-6.3, -1.0, 0]), np.array([0.3, -1.0, 0]), color=I.EDGE),
                      Line(np.array([1.8, -1.0, 0]), np.array([6.5, -1.0, 0]), color=I.EDGE))
        src = source("Microsoft Form 10-K FY2026 and 10-Q (September 2026); NextEra Form 10-K 2025", size=13)
        with self.voiceover(
            "Giant companies face the same arithmetic. <bookmark mark='a'/> Microsoft, in the year to June 2026, "
            f"reported {say_bn(M['ni'])} of net income, and its operations brought in {say_bn(M['ocf'])} of cash, "
            "more than its profit, because the wear on its equipment is a cost that does not drain cash, and "
            f"customers pay for subscriptions in advance. <bookmark mark='b'/> But it spent {say_bn(M['capex'])} on "
            "data centres, chips and buildings for artificial intelligence, almost twice as much as a year before. "
            f"<bookmark mark='c'/> What was left, the free cash, was {say_bn(M['fcf'])}, half its profit. And in the "
            "first quarter of the next year, free cash fell again, as spending kept rising. <bookmark mark='d'/> "
            "NextEra, the power company, spends far more than its operations bring in, every year: "
            f"{say_bn(N['capex'])} on new plants and wires in 2025 against {say_bn(N['ocf'])} of operating cash. The "
            "difference is borrowed, and repaid over decades from the bills of customers who have little choice of "
            "supplier. A utility is built to be cash-hungry; a software company is not, and for the AI build-out, "
            "Microsoft has chosen to become a little more like a utility."
        ) as vo:
            self.play(FadeIn(src), Create(axis))
            vo.wait_until("a")
            self.play(FadeIn(h1), *[AnimationGroup(FadeIn(bars[j], shift=UP * 0.05), FadeIn(labs[j]), FadeIn(vals[j]))
                                    for j in (0, 1)])
            vo.wait_until("b")
            self.play(FadeIn(bars[2], shift=DOWN * 0.05), FadeIn(labs[2]), FadeIn(vals[2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[3], shift=UP * 0.05), FadeIn(labs[3]), FadeIn(vals[3]), FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(h2), FadeIn(n2), LaggedStart(*[AnimationGroup(FadeIn(bars2[j]), FadeIn(labs2[j]),
                                                                       FadeIn(vals2[j])) for j in range(3)],
                                                          lag_ratio=0.4), run_time=2.2)
        self.clear_scene()
