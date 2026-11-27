from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

LINES = [("new", "new cars", DEALER), ("used", "used cars", "#4FA36A"), ("ps", "parts and service", SUPPLIER),
         ("fi", "finance and insurance", FINANCE)]


class Dealers(VoiceoverScene):
    def construct(self):
        card(self, 8, "The dealer", "How does a car dealer make its money, if not on new cars?",
             "Chapter eight. The dealer. How does a car dealer make its money, if not on new cars?", lit=("dollar", "moat"))
        self.mix()
        self.per_car()
        self.law()

    def _stack(self, shares, x, h=5.0, w=1.6):
        g, y = VGroup(), -h / 2 - 0.3
        for k, name, col in LINES:
            hh = h * shares[k]
            g.add(Rectangle(width=w, height=hh, stroke_color="#0E1117", stroke_width=1.5, fill_color=col, fill_opacity=0.92)
                  .move_to([x, y + hh / 2, 0]))
            y += hh
        return g

    def mix(self):
        D = R["dealers"]
        rs, gs = self._stack(D["rev_share"], -2.2), self._stack(D["gp_share"], 2.2)
        lr = VGroup(*[tx(f"{100 * D['rev_share'][k]:.0f}%", 15, WHITE, bold=True).move_to(r_) for (k, _, _), r_ in zip(LINES, rs)])
        lg = VGroup(*[tx(f"{100 * D['gp_share'][k]:.0f}%", 15, WHITE, bold=True).move_to(r_) for (k, _, _), r_ in zip(LINES, gs)])
        for t_, r_ in list(zip(lr, rs)) + list(zip(lg, gs)):
            if r_.height < 0.35:
                t_.scale(0.8)
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.92), tx(n, 15, WHITE)).arrange(RIGHT, buff=0.12)
                       for _, n, c in LINES]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.4, 0.0, 0])
        h1 = VGroup(tx("revenue", 18, WHITE, bold=True), tx(f"${sum(D['rev'].values()) / 1000:.1f}bn", 15, GREY_A)).arrange(DOWN, buff=0.04).next_to(rs, UP, buff=0.15)
        h2 = VGroup(tx("gross profit", 18, WHITE, bold=True), tx(f"${sum(D['gp'].values()) / 1000:.1f}bn", 15, GREY_A)).arrange(DOWN, buff=0.04).next_to(gs, UP, buff=0.15)
        shop = draw.showroom(2.2, sign="DEALER").move_to([-5.4, 1.6, 0])
        src = source("AutoNation, Form 10-K 2025", size=12)
        m = D["margin"]
        with self.voiceover(
            "America's established carmakers sell through franchised dealers: independent businesses holding a franchise "
            "for a brand. AutoNation, one of the largest, owned 323 franchises in 245 stores at the end of 2025. "
            "<bookmark mark='a'/> Here is its revenue in 2025, by what it sold: almost half "
            "from new cars, more than a quarter from used cars, the rest from parts and service and from arranging loans "
            f"and insurance. <bookmark mark='b'/> Now its gross profit. On a new car it kept only {100 * m['new']:.1f} "
            f"per cent. On used cars, {100 * m['used']:.1f}. <bookmark mark='c'/> But almost half of all its gross profit "
            f"came from parts and service, fixing the cars it and others had sold, at a margin of {100 * m['ps']:.0f} per "
            "cent. <bookmark mark='d'/> And almost a third came from finance and insurance: the commission for arranging "
            "the buyer's loan, the extended warranty, the service plan. The new car is the reason you walk in. The money "
            "is made after."
        ) as vo:
            self.play(FadeIn(shop), FadeIn(src), FadeIn(key), FadeIn(ghost(rs, gs, opacity=0.35)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in rs], lag_ratio=0.2), FadeIn(h1), run_time=2.0)
            self.play(FadeIn(lr))
            vo.wait_until("b")
            self.play(FadeIn(h2), GrowFromEdge(gs[0], DOWN), GrowFromEdge(gs[1], DOWN), FadeIn(lg[0]), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(gs[2], DOWN), FadeIn(lg[2]), FadeIn(draw.wrench(0.6).next_to(gs[2], RIGHT, buff=0.15)))
            vo.wait_until("d")
            self.play(GrowFromEdge(gs[3], DOWN), FadeIn(lg[3]))
        self.clear_scene()

    def per_car(self):
        D = R["dealers"]
        pc = D["per_car"]
        pa = viz.plot_axes([2022.5, 2025.5], [0, 5000], x_length=6.0, y_length=4.0, xticks=[2023, 2024, 2025],
                           yticks=[0, 1000, 2000, 3000, 4000, 5000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}",
                           ylabel="AutoNation's gross profit per new car", size=13).move_to([-3.0, -0.5, 0])
        bars_ = viz.year_bars(pa, [2023, 2024, 2025], [pc[2023], pc[2024], pc[2025]], DEALER, width=0.6)
        labs = VGroup(*[tx(f"${pc[y]:,.0f}", 15, DEALER, bold=True).next_to(b, UP, buff=0.08) for y, b in zip((2023, 2024, 2025), bars_)])
        C = D["census"]
        stats = VGroup(tx("America's new-car dealers, 2022", 18, WHITE, bold=True),
                       tx(f"{C['firms']:,.0f} companies, {C['stores']:,.0f} dealerships", 16, GREY_A),
                       tx(f"${C['sales'] / 1000:.2f} trillion of sales", 16, DEALER, bold=True),
                       tx(f"{C['staff']:,.0f} employees", 16, DEALER, bold=True),
                       tx(f"(car assembly: {R['making']['employees']:,.0f}; parts: {R['suppliers']['census']['parts'][1]:,.0f})", 14, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 0.2, 0])
        src = source("AutoNation, Form 10-K 2025; US Census Bureau, 2022 Economic Census (NAICS 441110, 336110, 3363)", size=12)
        with self.voiceover(
            "Even the thin margin on new cars moves with the shortage. <bookmark mark='a'/> In 2023, with lots still short "
            f"of cars, AutoNation made {pc[2023]:,.0f} dollars of gross profit on each new car it sold. In 2025, "
            f"{pc[2025]:,.0f}. <bookmark mark='b'/> Dealers are a big business in their own right. In 2022 America had "
            f"{C['firms']:,.0f} new-car dealer companies with {C['stores']:,.0f} dealerships, selling "
            f"{C['sales'] / 1000:.1f} trillion dollars' worth of cars, parts and service a year, and employing "
            f"{C['staff']:,.0f} people: more than the assembly plants and the parts makers together."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(bars_, opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(labs))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()

    def law(self):
        get("lcid.dealer_law")
        get("an.stores")
        maker = VGroup(draw.factory(1.5, MAKER), tx("carmaker", 15, MAKER, bold=True)).arrange(DOWN, buff=0.08).move_to([-5.0, 0.6, 0])
        shop = VGroup(draw.showroom(1.9), tx("franchised dealer", 15, DEALER, bold=True)).arrange(DOWN, buff=0.08).move_to([0.0, 0.6, 0])
        buyer = VGroup(draw.person(0.8, "#C9D3E0"), tx("buyer", 15, WHITE, bold=True)).arrange(DOWN, buff=0.08).move_to([5.0, 0.6, 0])
        a1 = Arrow(maker.get_right(), shop.get_left(), buff=0.2, color=GREY_B, stroke_width=3)
        a2 = Arrow(shop.get_right(), buyer.get_left(), buff=0.2, color=GREY_B, stroke_width=3)
        direct = CurvedArrow(maker.get_top() + UP * 0.1, buyer.get_top() + UP * 0.1, angle=-0.6, color=EV, stroke_width=3)
        dl = tx("direct sales: Tesla, Rivian, Lucid", 16, EV, bold=True).move_to([0, 2.8, 0])
        quote = VGroup(tx("Lucid, Form 10-K 2025: 'state laws ... generally require motor vehicle manufacturers and dealers to be", 14, WHITE),
                       tx("licensed in order to sell vehicles directly to residents. Certain states do not permit automobile", 14, WHITE),
                       tx("manufacturers to be licensed as dealers'", 14, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([0, -2.0, 0])
        src = source("Lucid Group, Form 10-K 2025", size=12)
        with self.voiceover(
            "Why does the carmaker not sell to you directly and keep the dealer's share? <bookmark mark='a'/> Partly "
            "history: the established makers built their sales on independent dealers, who put up the money for the "
            "showrooms, the stock on the lots and the service bays. <bookmark mark='b'/> And partly law. Lucid's annual "
            "report explains that America's states license who may sell cars to their residents, and that some states do "
            "not let a carmaker be licensed as a dealer at all. <bookmark mark='c'/> The newcomers, Tesla, Rivian and "
            "Lucid, sell directly where the law allows, and Lucid's report warns that dealers may challenge it where the "
            "law is unclear. The established makers, with thousands of dealers under contract, cannot easily follow."
        ) as vo:
            self.play(FadeIn(maker), FadeIn(shop), FadeIn(buyer), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("b")
            self.play(FadeIn(quote))
            vo.wait_until("c")
            self.play(Create(direct), FadeIn(dl))
        self.clear_scene()
