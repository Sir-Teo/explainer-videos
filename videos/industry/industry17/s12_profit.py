from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Profit(VoiceoverScene):
    def construct(self):
        card(self, 10, "Where the profit is", "Which vehicles actually make money?",
             "Chapter ten. Where the profit is. Which vehicles actually make money?", lit=("dollar", "moat"))
        self.mix()
        self.ford()
        self.luxury()

    def mix(self):
        P = R["profit"]
        us, gm = P["us"], P["gm_us"]
        kinds = [("cars", draw.car(1.6, MAKER), us["cars"], gm["cars"]), ("crossovers", draw.suv(1.6, GOOD), us["crossovers"], gm["crossovers"]),
                 ("trucks", draw.pickup(1.7, BAD), us["trucks"], gm["trucks"])]
        g = VGroup()
        for i, (n, icon, tot, mine) in enumerate(kinds):
            x = -4.3 + 4.3 * i
            icon.move_to([x, 1.7, 0])
            share = VGroup(tx(f"{100 * tot / us['total']:.0f}%", 40, WHITE, bold=True), tx(f"of US sales ({tot / 1000:.1f}m)", 15, GREY_A)).arrange(DOWN, buff=0.06).move_to([x, 0.15, 0])
            gms = VGroup(tx("GM's share:", 15, MAKER), tx(f"{100 * mine / tot:.1f}%", 26, MAKER, bold=True)).arrange(DOWN, buff=0.04).move_to([x, -1.55, 0])
            g.add(VGroup(icon, tx(n, 18, PRICE, bold=True).next_to(icon, DOWN, buff=0.1), share, gms))
        head = tx(f"What Americans bought in 2025: {us['total'] / 1000:.1f} million vehicles", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("General Motors, Form 10-K 2025 (industry and GM sales by type, United States)", size=12)
        with self.voiceover(
            "Start with what people buy. <bookmark mark='a'/> In America in 2025, only "
            f"{100 * us['cars'] / us['total']:.0f} per cent of new vehicles were cars in the old sense: saloons, hatchbacks, "
            f"coupés. <bookmark mark='b'/> {100 * us['crossovers'] / us['total']:.0f} per cent were crossovers, tall family "
            f"vehicles somewhere between a car and an SUV, <bookmark mark='c'/> and {100 * us['trucks'] / us['total']:.0f} per cent were "
            "trucks: pickups and big sport utility vehicles. <bookmark mark='d'/> General Motors sold a third of all the "
            f"trucks, and almost no cars, {100 * gm['cars'] / us['cars']:.1f} per cent of that market. General Motors, "
            "with 17.2 per cent of the whole American market, has followed the money out of the car and into the truck."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(*[k[0] for k in g], opacity=0.3)))
            for mk, k in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(k[0]), FadeIn(k[1]), FadeIn(k[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(k[3]) for k in g], lag_ratio=0.3))
            self.play(Indicate(g[2][3], color=PRICE))
        self.clear_scene()

    def ford(self):
        F = R["profit"]["ford"]
        names = {"blue": ("Ford Blue", "petrol and hybrid cars for households", MAKER, draw.suv(1.3, MAKER)),
                 "pro": ("Ford Pro", "trucks and vans for businesses and fleets", PRICE, draw.pickup(1.4, PRICE)),
                 "e": ("Ford Model e", "electric vehicles", EV, draw.battery_pack(1.3, color=EV))}
        rows = VGroup()
        for i, k in enumerate(("blue", "pro", "e")):
            units, rev, ebit = F[k]
            per = ebit * 1e3 / units
            y = 1.7 - 1.7 * i
            n, what, col, icon = names[k]
            icon.move_to([-5.6, y, 0])
            lab = VGroup(tx(n, 19, col, bold=True), tx(what, 14, GREY_A),
                         tx(f"{units:,.0f}k vehicles, EBIT {'-' if ebit < 0 else ''}${abs(ebit) / 1e3:.1f}bn", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-4.6, y, 0], aligned_edge=LEFT)
            b = bar(1.2, y, np.sign(per) * max(abs(per) * 2.4 / 10_000, 0.05), 0.5, GOOD if per > 0 else BAD)
            val = tx(usd(per) + " a vehicle", 18, GOOD if per > 0 else BAD, bold=True).next_to(b, RIGHT if per > 0 else LEFT, buff=0.12)
            rows.add(VGroup(icon, lab, b, val))
        axis = Line([1.2, 2.5, 0], [1.2, -2.5, 0], stroke_color=GREY_B, stroke_width=2)
        head = tx("Ford, 2025: one company, three businesses", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Ford Motor Company, Form 10-K 2025 (segment wholesale units and EBIT)", size=12)
        b_, p_, e_ = (F[k][2] * 1e3 / F[k][0] for k in ("blue", "pro", "e"))
        with self.voiceover(
            "Ford splits itself in three, and the split shows where the money is. <bookmark mark='a'/> Ford Blue sells "
            f"petrol and hybrid cars to households: in 2025 it earned about {b_:,.0f} dollars on each vehicle. "
            "<bookmark mark='b'/> Ford Pro sells pickups and vans to businesses, fleets and governments, along with the "
            f"servicing: about {p_:,.0f} dollars a vehicle, four times as much. <bookmark mark='c'/> And Ford Model e, its electric vehicles, lost about "
            f"{-e_:,.0f} dollars on each one it sold. Hold on to that number; it is the next chapter."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(head), FadeIn(src), FadeIn(ghost(*[r_[:2] for r_ in rows], opacity=0.3)))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0]), FadeIn(r_[1]), GrowFromEdge(r_[2], LEFT if r_[2].get_center()[0] > 1.2 else RIGHT), FadeIn(r_[3]))
        self.clear_scene()

    def luxury(self):
        P = R["profit"]
        fe = P["ferrari"]
        fer = fe["op"] * 1e9 / fe["units"]
        toy = P["toyota"]["op"] * 1e9 / P["toyota"]["units"]
        hm = P["honda"]
        left = VGroup(draw.car(2.4, BAD), tx("Ferrari, 2025", 20, WHITE, bold=True),
                      tx(f"{fe['units']:,.0f} cars", 16, GREY_A),
                      tx(f"€{fer:,.0f}", 40, GOOD, bold=True), tx("operating profit per car", 15, GREY_A)).arrange(DOWN, buff=0.12).move_to([-4.3, 0.3, 0])
        mid = VGroup(draw.car(2.0, MAKER), tx("Toyota's car business", 20, WHITE, bold=True),
                     tx(f"{P['toyota']['units'] / 1e6:.2f} million vehicles", 16, GREY_A),
                     tx(f"¥{toy:,.0f}", 40, GOOD, bold=True), tx(f"about ${toy / P['toyota']['jpy']:,.0f} per vehicle", 15, GREY_A)).arrange(DOWN, buff=0.12).move_to([0.0, 0.3, 0])
        bike = VGroup(Circle(radius=0.28, stroke_color=PRICE, stroke_width=4), Circle(radius=0.28, stroke_color=PRICE, stroke_width=4).shift(RIGHT * 1.0),
                      Line([0, 0, 0], [0.45, 0.35, 0], stroke_color=PRICE, stroke_width=4), Line([0.45, 0.35, 0], [1.0, 0, 0], stroke_color=PRICE, stroke_width=4),
                      Line([0.3, 0.35, 0], [0.75, 0.35, 0], stroke_color=PRICE, stroke_width=6))
        right = VGroup(bike, tx("Honda, year to March 2026", 20, WHITE, bold=True),
                       tx(f"motorcycles: {hm['moto'][0] / 1e3:.1f}m, ¥{hm['moto'][2]:,.0f}bn profit", 16, PRICE, bold=True),
                       tx(f"cars: {hm['auto'][0] / 1e3:.1f}m, ¥{hm['auto'][2]:,.0f}bn", 16, BAD, bold=True),
                       tx(f"motorcycle margin {100 * hm['moto'][2] / hm['moto'][1]:.0f}%", 15, GREY_A)).arrange(DOWN, buff=0.12).move_to([4.4, 0.3, 0])
        src = source("Ferrari and Toyota, Forms 20-F; Honda, Form 20-F for the year to March 2026 (segment operating profit)", size=12)
        with self.voiceover(
            "At the other extreme is luxury. <bookmark mark='a'/> Ferrari shipped "
            f"{fe['units']:,.0f} cars in 2025 and made {fer:,.0f} euros of operating profit on each. It keeps its "
            "volumes down on purpose, a 'controlled volume strategy', in its own words, to keep the brand exclusive. "
            f"<bookmark mark='b'/> Toyota's car business made about {toy / P['toyota']['jpy']:,.0f} dollars on each of its "
            f"{P['toyota']['units'] / 1e6:.1f} million. <bookmark mark='c'/> And the strangest number in the business: in "
            f"the year to March 2026, Honda sold {hm['moto'][0] / 1e3:.1f} million motorcycles and made "
            f"{hm['moto'][2]:,.0f} billion yen on them, while its car business, with {hm['auto'][0] / 1e3:.1f} million "
            f"cars, lost {-hm['auto'][2]:,.0f} billion. Same company, same brand; different business."
        ) as vo:
            self.play(FadeIn(src), FadeIn(left[:2]), FadeIn(mid[:2]), FadeIn(right[:2]), FadeIn(ghost(left[2:], mid[2:], right[2:], opacity=0.35)))
            vo.wait_until("a")
            self.play(FadeIn(left[2:], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(mid[2:], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(right[2:], shift=UP * 0.1))
        self.clear_scene()
