from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403


class Costco(VoiceoverScene):
    def construct(self):
        card(self, 6, "Paid before it pays", "How does a shop that keeps under four cents a dollar earn so much?",
             "Chapter six. Paid before it pays.", lit=("dollar", "moat"))
        self.timeline()
        self.members()

    def timeline(self):
        C = R["costco"]
        x0, s = -6.0, 0.36
        axis = Arrow(np.array([x0 - 0.2, 0, 0]), np.array([x0 + 36 * s, 0, 0]), buff=0, color=I.EDGE, stroke_width=2,
                     max_tip_length_to_length_ratio=0.03)
        ticks = VGroup(*[VGroup(Line(np.array([x0 + d * s, -0.08, 0]), np.array([x0 + d * s, 0.08, 0]), color=I.FAINT),
                                T(f"day {d}", 14, I.DIM).next_to(np.array([x0 + d * s, -0.1, 0]), DOWN, buff=0.08))
                         for d in (0, 10, 20, 30)])

        def event(day, text, color, up=True, dy=1.2, side=None):
            p = np.array([x0 + day * s, 0, 0])
            stem = Line(p, p + UP * (dy if up else -dy), color=color, stroke_width=2)
            dot = Dot(p, color=color, radius=0.08)
            lab = VGroup(*[TB(t, 18, color) if i == 0 else T(t, 16, I.TEXT) for i, t in enumerate(text)]).arrange(
                DOWN, buff=0.04, aligned_edge=RIGHT if side == "left" else (LEFT if side == "right" else ORIGIN))
            if side == "left":
                lab.next_to(stem.get_end(), LEFT, buff=0.12).align_to(stem.get_end(), UP)
            elif side == "right":
                lab.next_to(stem.get_end(), RIGHT, buff=0.12).align_to(stem.get_end(), UP)
            else:
                lab.next_to(stem, UP if up else DOWN, buff=0.08)
            return VGroup(stem, dot, lab)
        e0 = event(0, ["goods arrive", "from the supplier"], "#7EC8F5", up=True, dy=0.8)
        e1 = event(C["inventory_days"], [f"day {C['inventory_days']:.0f}", "sold, on average;", "members pay at the till"],
                   I.PROFIT, up=True, dy=2.0, side="left")
        e2 = event(C["payable_days"], [f"day {C['payable_days']:.0f}", "Costco pays", "the supplier"], I.COST, up=True,
                   dy=1.0, side="right")
        gap = Brace(Line(np.array([x0 + C["inventory_days"] * s, 0, 0]), np.array([x0 + C["payable_days"] * s, 0, 0])),
                    DOWN, buff=0.45, color=I.ACCENT)
        gap_t = T("the supplier's money, Costco's to use", 16, I.ACCENT).next_to(gap, DOWN, buff=0.1)
        side = VGroup(T(f"Stock on the shelves: {bn(get('cost.inventory'))}", 19, I.TEXT),
                      T(f"Owed to suppliers: {bn(get('cost.payables'))}", 19, I.TEXT),
                      T(f"Cash in the bank: {bn(get('cost.cash'))}", 19, I.TEXT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.45)
        head = T("Costco, fiscal 2026: how long the money waits", 24, I.TEXT).to_corner(UL, buff=0.4)
        src = source("Costco Form 10-K FY2026; days computed from merchandise costs, inventories and payables",
                     size=13)
        with self.voiceover(
            f"Costco keeps less than four cents of each dollar of sales. Yet it earned {say_bn(get('cost.ni'))} "
            "in its last fiscal year. Two things explain it, and both are in the accounts. <bookmark mark='a'/> The "
            "first is time. A pallet of goods arrives at a Costco warehouse. <bookmark mark='b'/> On average it is "
            f"sold within about {C['inventory_days']:.0f} days, and members pay at the till, on the spot. "
            f"<bookmark mark='c'/> Costco pays its supplier after about {C['payable_days']:.0f} days. <bookmark "
            "mark='d'/> So Costco has been paid before it pays. Across the whole company, the money it owes "
            f"suppliers, {say_bn(get('cost.payables'))}, is larger than all the stock on its shelves. Its suppliers, "
            "in effect, finance its shelves, and the faster it grows, the more of their money it holds. The bakery "
            "that gave cafes sixty days ran out of cash; Costco gets the opposite deal."
        ) as vo:
            # a pallet rides the timeline: stock until it sells, then members' cash until the supplier is paid
            row_y = -2.25
            pallet = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.26, height=0.22, stroke_color="#0E1117",
                                               stroke_width=1, fill_color="#7EC8F5", fill_opacity=0.95)
                              for _ in range(6)]).arrange_in_grid(rows=2, cols=3, buff=0.02)
            pallet.add(Rectangle(width=0.86, height=0.06, stroke_width=0, fill_color="#A0855B", fill_opacity=1).next_to(
                pallet, DOWN, buff=0))
            truck = draw.truck(1.2).move_to([x0 - 3.0, row_y + 0.1, 0])
            pallet.move_to([x0, row_y, 0])
            cash = draw.coin_stack(6, 0.16)
            buyers = draw.crowd(4, 0.36, cols=4).move_to([x0 + C["inventory_days"] * s - 1.7, row_y - 0.95, 0])
            supplier = VGroup(draw.factory(0.9, color="#7EC8F5"), T("supplier", 15, I.DIM)).arrange(DOWN, buff=0.04)
            supplier.move_to([6.35, row_y - 0.85, 0])
            self.play(FadeIn(head), FadeIn(src), Create(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(e0), truck.animate.move_to([x0 - 0.6, row_y + 0.1, 0]), run_time=1.2)
            self.play(FadeIn(pallet, shift=RIGHT * 0.3), FadeOut(truck, shift=LEFT * 0.5))
            vo.wait_until("b")
            self.play(pallet.animate.move_to([x0 + C["inventory_days"] * s, row_y, 0]), FadeIn(e1),
                      FadeIn(buyers), run_time=2.0, rate_func=linear)
            cash.move_to(pallet)
            self.play(ReplacementTransform(pallet, cash), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(supplier))
            self.play(cash.animate.move_to([x0 + C["payable_days"] * s, row_y, 0]), FadeIn(e2), run_time=1.0,
                      rate_func=linear)
            self.play(cash.animate.move_to(supplier.get_left()).scale(0.6), run_time=0.9)
            self.play(FadeOut(cash))
            vo.wait_until("d")
            self.play(GrowFromCenter(gap), FadeIn(gap_t), FadeIn(side))
        self.clear_scene()

    def members(self):
        C = R["costco"]
        pm = C["per_member"]
        merch = pm["oi"] - pm["fee"]
        big = VGroup(TB(f"${pm['spend']:,.0f}", 54, I.TEXT), T("spent by each paid member in a year", 20, I.DIM)
                     ).arrange(DOWN, buff=0.1).move_to(LEFT * 3.4 + UP * 1.3)
        W = 4.6
        col = VGroup(
            Rectangle(width=1.4, height=W * merch / pm["oi"], fill_color="#7EC8F5", fill_opacity=0.9, stroke_width=0),
            Rectangle(width=1.4, height=W * pm["fee"] / pm["oi"], fill_color=I.ACCENT, fill_opacity=0.95,
                      stroke_width=0)).arrange(UP, buff=0).move_to(RIGHT * 2.2 + DOWN * 0.4)
        labs = VGroup(VGroup(TB(f"${merch:.0f}", 24, "#7EC8F5"), T("operating profit on the goods", 17, I.TEXT)
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(col[0], RIGHT, buff=0.3),
                      VGroup(TB(f"${pm['fee']:.0f}", 24, I.ACCENT), T("the membership fee", 17, I.TEXT)
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(col[1], RIGHT, buff=0.3))
        top = TB(f"${pm['oi']:.0f} of operating profit per member", 22, I.TEXT).next_to(col, UP, buff=0.2)
        facts = VGroup(T(f"{get('cost.members'):.1f} million paid members", 19, I.TEXT),
                       T(f"{get('cost.warehouses'):.0f} warehouses", 19, I.TEXT),
                       T(f"fees: {bn(C['fees'])}, {say_pct(C['fee_share']).replace(' percent', '%')} of operating "
                         "income", 19, I.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(
            LEFT * 3.4 + DOWN * 1.2)
        head = T("Costco per paid member, fiscal 2026", 24, I.TEXT).to_corner(UL, buff=0.4)
        src = source("Costco Form 10-K FY2026; per member: averages of the year's opening and closing paid members",
                     size=13)
        with self.voiceover(
            f"The second thing is the membership card. <bookmark mark='a'/> Costco had "
            f"{get('cost.members'):.1f} million paid members at the end of its 2026 fiscal year, and each one spent "
            f"about {say_usd(pm['spend'])} there in the year. <bookmark mark='b'/> On those purchases Costco made "
            f"about {say_usd(merch)} of operating profit. <bookmark mark='c'/> And each member also paid about "
            f"{say_usd(pm['fee'])} for the card itself. <bookmark mark='d'/> Membership fees were "
            f"{say_bn(C['fees'])}, {say_pct(C['fee_share'])} of Costco's operating income. Costco sells the goods "
            "with less than two cents of operating profit on each dollar, and earns half its profit selling the right "
            "to shop there. The low prices keep the "
            "members renewing, and the renewals pay for the low prices."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(big), FadeIn(facts[:2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(col[0], DOWN), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(col[1], DOWN), FadeIn(labs[1]), FadeIn(top))
            vo.wait_until("d")
            self.play(FadeIn(facts[2]), Indicate(col[1], color=I.ACCENT))
        self.clear_scene()
