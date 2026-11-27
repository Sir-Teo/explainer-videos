from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403

KEYS = [("h0_s0", "sell nothing ahead, sell at harvest"), ("h0_s1", "sell nothing ahead, store till June"),
        ("h50_s0", "sell half ahead, rest at harvest"), ("h50_s1", "sell half ahead, store the rest"),
        ("h100_s0", "sell it all ahead"), ("h100_s1", "sell it all ahead (nothing to store)")]


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: three seasons", "You grow corn. When do you sell it?",
             "Chapter one. Run it: three seasons.", lit=("make", "change"))
        self.setup_()
        for k in range(3):
            self.season(k)
        self.totals()

    def setup_(self):
        A = R["acre"]
        fld = draw.field(6.4, 3, 12, "corn", 0.7).move_to([-3.2, 0.9, 0])
        trac = draw.tractor(1.3).next_to(fld, DOWN, buff=0.15).align_to(fld, LEFT)
        farm_l = VGroup(tx(f"A {A['size']:.0f}-acre corn farm in Iowa", 20, WHITE, bold=True),
                        tx("(about the size of the average corn farm in USDA's survey)", 14, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(fld, UP, buff=0.2)
        c1 = VGroup(tx("In April, at planting:", 20, CORN, bold=True),
                    tx("sell none, half or all of the crop you expect,", 17, WHITE),
                    tx("at today's price for delivery after harvest", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        c2 = VGroup(tx("In October, at harvest:", 20, CORN, bold=True),
                    tx("sell what is left now, or keep it in a bin", 17, WHITE),
                    tx(f"until June, at {100 * R['run']['carry']:.0f} cents a bushel a month", 17, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        bin_ = draw.grain_elevator(1.3).scale(0.8)
        cards = VGroup(VGroup(c1, draw.sack(0.8, label_="SOLD").scale(0.9)).arrange(RIGHT, buff=0.4),
                       VGroup(c2, bin_).arrange(RIGHT, buff=0.4)).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(
            [3.5, 0.6, 0])
        warn = tx("Three real seasons, one after another. You choose before you see the weather or the price.", 17,
                  PRICE).to_edge(DOWN, buff=0.85)
        tag = estimate_tag("the Works (farm.py): USDA's costs, yields and harvest prices; the IMF's maize price for the "
                           "months between", corner=DR, size=13)
        with self.voiceover(
            "Play it yourself. You farm corn in Iowa, on about three hundred acres, the size of the typical corn farm "
            "in the Department of Agriculture's cost survey. <bookmark mark='a'/> Every spring you decide how much of "
            "the crop you expect to sell ahead, at today's price for delivery after harvest. That is called hedging, "
            "or forward selling. You can sell none of it, half, or all. <bookmark mark='b'/> And every autumn, whatever "
            "you have not already sold, you either sell at harvest or keep in a bin until the following June, hoping the "
            "price rises by more than the cost of storing it. <bookmark mark='c'/> You will play three real seasons, "
            "with the real yields, costs and prices of those years. You do not know which years they are. Pause, and "
            "choose a rule you will stick to."
        ) as vo:
            self.play(FadeIn(fld), FadeIn(farm_l), FadeIn(tag))
            self.play(FadeIn(trac, shift=RIGHT * 0.5))
            self.play(trac.animate.shift(RIGHT * 4.6), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(warn))
        self.clear_scene()

    def season(self, k):
        S = R["run"]["seasons"][k]
        y = S["year"]
        mz_months = R["futures"]["months"]
        bu = dict(zip(mz_months, R["futures"]["bu"]))
        ms = [f"{y}-{m:02d}" for m in range(4, 13)] + [f"{y + 1}-{m:02d}" for m in range(1, 7)]
        scale = S["harvest"] / bu[f"{y}-10"]
        path = [bu[m] * scale for m in ms]
        pa = viz.plot_axes([0, len(ms) - 1], [0, 8], x_length=5.6, y_length=3.0, xticks=[0, 6, 14],
                           yticks=[2, 4, 6, 8], xfmt=lambda v: ["April", "October", "next June"][[0, 6, 14].index(int(v))],
                           yfmt=lambda v: f"${v:g}", size=13).move_to([-3.5, 1.0, 0])
        pl = VMobject(stroke_color=PRICE, stroke_width=3.5).set_points_as_corners(
            [pa.ax.c2p(i, v) for i, v in enumerate(path)])
        pts = VGroup(Dot(pa.ax.c2p(0, S["plant"]), color=CORN), Dot(pa.ax.c2p(6, S["harvest"]), color=CORN),
                     Dot(pa.ax.c2p(14, S["later"]), color=CORN))
        pt_l = VGroup(tx(f"${S['plant']:.2f}", 14, CORN).next_to(pts[0], UP, buff=0.08),
                      tx(f"${S['harvest']:.2f}", 14, CORN).next_to(pts[1], UP, buff=0.08),
                      tx(f"${S['later']:.2f}", 14, CORN).next_to(pts[2], UP, buff=0.08))
        ptitle = tx("price of a bushel", 15, GREY_A).next_to(pa, UP, buff=0.08)
        yb = VGroup()
        for i, (lab, v, col) in enumerate([("expected", S["expected"], GREY_B), ("harvested", S["actual"], CORN)]):
            b = Rectangle(width=0.7, height=v / 200 * 1.6, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [-5.2 + 1.1 * i, -3.0, 0], aligned_edge=DOWN)
            yb.add(VGroup(b, tx(f"{v:.0f}", 15, WHITE, bold=True).next_to(b, UP, buff=0.05),
                          tx(lab, 13, GREY_A).next_to(b, DOWN, buff=0.06)))
        yt = tx("bushels an acre", 15, GREY_A).next_to(yb, UP, buff=0.3)
        cost = VGroup(tx("cost of growing an acre", 15, GREY_A), tx(f"${S['cost']:.0f}", 22, COST, bold=True)).arrange(
            DOWN, buff=0.04).move_to([-1.9, -2.0, 0])
        rows = VGroup()
        for key, lab in KEYS[:5]:
            v = S["outcomes"][key]
            rows.add(VGroup(tx(lab, 16, WHITE), tx(f"{'+' if v >= 0 else '-'}${abs(v):,.0f}", 18, GREEN_C if v >= 0 else STATE,
                                                   bold=True)))
        for i, r_ in enumerate(rows):
            r_[0].move_to([3.0, 1.6 - 0.6 * i, 0], aligned_edge=LEFT).shift(LEFT * 1.2)
            r_[1].move_to([6.3, 1.6 - 0.6 * i, 0], aligned_edge=RIGHT)
        rh = tx("profit or loss an acre, after all costs", 16, GREY_A).move_to([4.0, 2.3, 0])
        best = max(range(5), key=lambda i: S["outcomes"][KEYS[i][0]])
        box = SurroundingRectangle(rows[best], color=PRICE, buff=0.08)
        head = tx(f"Season {k + 1}: {y}", 26, PRICE, bold=True).to_edge(UP, buff=0.35)
        say = {
            2012: ("Season one. You plant expecting about a hundred and fifty bushels an acre. Then the worst drought in "
                   "decades settles on the Corn Belt. <bookmark mark='a'/> The harvest is a hundred and eighteen "
                   "bushels. <bookmark mark='b'/> But because the whole Corn Belt is short, the price soars, from "
                   f"{say_money(S['plant'])} at planting to {say_money(S['harvest'])} at harvest. <bookmark mark='c'/> "
                   "If you sold your expected crop ahead, you now have to buy back corn you never grew, at the higher "
                   "price, to fill your contract: a loss. If you sold nothing ahead, the high price makes up for the "
                   "small crop, and you make money. Storing until June costs you, because the price drifts down."),
            2014: ("Season two. <bookmark mark='a'/> Near-perfect weather: a hundred and seventy bushels an acre, far more "
                   "than you expected, and the same everywhere else. <bookmark mark='b'/> So the price collapses, from "
                   f"{say_money(S['plant'])} in April to {say_money(S['harvest'])} at harvest. "
                   "<bookmark mark='c'/> Now the forward sale is the hero: every bushel sold in spring earned the spring "
                   "price. Selling nothing ahead loses almost ninety dollars an acre. A record crop, and a loss: that is "
                   "farming."),
            2020: ("Season three. <bookmark mark='a'/> A slightly disappointing crop, a hundred and seventy-eight "
                   f"bushels, and a weak price in spring, {say_money(S['plant'])}, because a pandemic has closed the "
                   "world's restaurants and ethanol plants. <bookmark mark='b'/> Then, after harvest, China begins buying "
                   "American corn on a record scale and the price takes off, to "
                   f"{say_money(S['later'])} by the next June. <bookmark mark='c'/> Selling ahead was the worst choice "
                   "of the six. Keeping the grain in a bin and waiting earned more than two hundred and seventy dollars "
                   "an acre."),
        }[y]
        src = source(f"USDA ERS commodity costs and returns, corn, {y} (US total); IMF maize price via FRED for the "
                     "months between", size=13)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(ptitle), FadeIn(src), FadeIn(rh), FadeIn(cost),
                      FadeIn(VGroup(*[r_[0] for r_ in rows])))
            self.play(GrowFromEdge(yb[0][0], DOWN), FadeIn(yb[0][1:]), FadeIn(yt))
            vo.wait_until("a")
            self.play(GrowFromEdge(yb[1][0], DOWN), FadeIn(yb[1][1:]))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pt_l[0]))
            self.play(Create(pl), run_time=3.0, rate_func=linear)
            self.play(FadeIn(pts[1:]), FadeIn(pt_l[1:]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[1], shift=LEFT * 0.15) for r_ in rows], lag_ratio=0.25), run_time=2.0)
            self.play(Create(box))
        self.clear_scene()

    def totals(self):
        T = R["run"]["totals"]
        order = sorted(T, key=T.get, reverse=True)
        labs = dict(KEYS)
        bars = VGroup()
        mx_ = max(abs(v) for v in T.values())
        for i, key in enumerate(k for k in order if k != "h100_s1"):
            v = T[key]
            w = 3.2 * abs(v) / mx_
            b = Rectangle(width=max(w, 0.02), height=0.45, stroke_width=0, fill_color=GREEN_C if v >= 0 else STATE,
                          fill_opacity=0.9)
            b.move_to([1.6, 1.6 - 0.7 * i, 0], aligned_edge=LEFT if v >= 0 else RIGHT)
            bars.add(VGroup(b, tx(labs[key], 17, WHITE).next_to([1.4, 1.6 - 0.7 * i, 0], LEFT, buff=0.1).shift(LEFT * 0.0),
                            tx(f"{'+' if v >= 0 else '-'}${abs(v):.0f}", 17, WHITE, bold=True).next_to(
                                b, RIGHT if v >= 0 else LEFT, buff=0.1)))
        for b in bars:
            b[1].next_to([-0.5, b[0].get_center()[1], 0], LEFT, buff=0.1)
        axis = Line([1.6, 2.0, 0], [1.6, -1.6, 0], stroke_color=GREY_B, stroke_width=1.5)
        head = tx("Three seasons together: profit an acre", 24, WHITE, bold=True).to_edge(UP, buff=0.45)
        lesson = VGroup(tx("No rule wins every year.", 22, PRICE, bold=True),
                        tx("A forward sale removes the price risk, but not the weather:", 18, WHITE),
                        tx("in a drought it becomes a bet. That is why most farmers also", 18, WHITE),
                        tx("buy crop insurance that pays on their revenue, not just their yield.", 18, WHITE)).arrange(
            DOWN, buff=0.08).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("the Works (farm.py); storage at 4 cents a bushel a month is an assumption", corner=DR, size=13)
        with self.voiceover(
            "Add the three seasons together. <bookmark mark='a'/> Over these three years, selling nothing ahead and "
            f"storing until June did best, about {T['h0_s1']:.0f} dollars an acre. Selling everything ahead did worst. "
            "But change the three years and the ranking changes. <bookmark mark='b'/> What the game shows is that no "
            "rule wins every year. A forward sale takes away the risk of the price, but not the risk of the weather, "
            "and in a drought, a hedge on a crop you did not grow becomes a bet. That is why most American corn "
            "farmers also buy crop insurance that pays when their revenue falls, not just their yield. Notice too how "
            "small the numbers are. In two of the three years the farm barely covered its costs, whatever it did. The "
            "price is set somewhere else, by millions of farmers and the weather on several continents, and one farmer "
            "can only choose how to live with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], LEFT if T[k] >= 0 else RIGHT), FadeIn(b[1:]))
                                    for b, k in zip(bars, [k for k in order if k != "h100_s1"])], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()
