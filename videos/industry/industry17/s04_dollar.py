from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 3, "Where a car's dollar goes", "Of the price of a new car, who gets what?",
             "Chapter three. Where a car's dollar goes. Of the price of a new car, who gets what?", lit=("dollar",))
        self.column()
        self.bought()

    def column(self):
        D = R["dollar"]
        sp, price = D["split"], D["price"]
        items = [("the parts and materials the maker buys", sp["materials"] * price, SUPPLIER,
                  f"{100 * D['mat_share']:.0f}% of what the assembly plants ship (Census)"),
                 ("the assembly plants' payroll", sp["payroll"] * price, MAKER, f"{100 * D['pay_share']:.1f}% of shipments (Census)"),
                 ("everything else at the maker", sp["rest"] * price, "#4A6A8A",
                  "engineering, tooling, warranty, marketing, overhead, profit"),
                 ("the dealer's gross margin on the car", sp["dealer"] * price, DEALER, "AutoNation, 2025")]
        col = viz.DollarColumn(items, total=price, height=5.6, width=1.4, label_x=0.9, size=18, fmt=lambda v: usd(v),
                               label_width=6.2).move_to([-1.6, -0.35, 0])
        top = col.top_label(f"{usd(price)}: the average new car at AutoNation, 2025", 20, PRICE)
        car_ = draw.suv(2.2, MAKER).move_to([-5.3, 1.6, 0])
        prof = VGroup(tx("of which the maker's profit:", 15, GREY_A),
                      tx(f"GM North America {100 * D['gmna']:.1f}%", 17, MAKER, bold=True),
                      tx(f"Ford Blue {100 * D['blue']:.1f}% of revenue (2025)", 17, MAKER, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        prof.move_to([-6.6, -1.2, 0], aligned_edge=LEFT)
        if prof.get_right()[0] > -2.6:
            prof.scale_to_fit_width(3.9).move_to([-6.6, -1.2, 0], aligned_edge=LEFT)
        src = source("AutoNation, Form 10-K 2025; US Census Bureau, 2022 Economic Census (car and light-truck assembly); GM and "
                     "Ford, Forms 10-K 2025 (segment EBIT)", size=12)
        tag = estimate_tag("estimate: shares from different sources put together", size=13)
        with self.voiceover(
            f"Take the average new car that AutoNation, one of America's largest car retailers, sold in 2025: {price:,.0f} "
            f"dollars. <bookmark mark='a'/> The dealer kept about {100 * sp['dealer']:.0f} cents in the dollar as gross "
            "margin on the car itself; we will see later where the dealer really makes its money. <bookmark mark='b'/> The "
            "rest went to the carmaker. And here is the surprise. For every dollar of cars the assembly plants shipped, "
            f"they had paid about {100 * D['mat_share']:.0f} cents to other companies, for parts and materials. "
            f"<bookmark mark='c'/> Their own payroll was about {100 * D['pay_share']:.1f} cents. <bookmark mark='d'/> What "
            "is left has to pay for designing the car, tooling the plant, the warranty, the marketing and the head office, "
            f"with profit last. In 2025 General Motors' North American business kept {100 * D['gmna']:.1f} cents of each "
            f"dollar of revenue as operating profit, and the petrol side of Ford, {100 * D['blue']:.1f}. A carmaker is, "
            "more than anything, a buyer and an assembler of other companies' work."
        ) as vo:
            self.play(FadeIn(car_), FadeIn(top), FadeIn(src), FadeIn(tag), FadeIn(ghost(col.slices, opacity=0.3)))
            order = [3, 0, 1, 2]
            for mk, k in zip("abcd", order):
                vo.wait_until(mk)
                self.play(FadeIn(col.slices[k]), Create(col.leaders[k]), FadeIn(col.labels[k], shift=LEFT * 0.1))
            self.play(FadeIn(prof))
        self.clear_scene()

    def bought(self):
        D = R["dollar"]
        mats = list(D["materials"].items())[:8] + [("semiconductors and related devices",
                                                     D["materials"]["semiconductors and related devices"])]
        mx = mats[0][1]
        rows = VGroup()
        for i, (n, v) in enumerate(mats):
            y = 2.0 - 0.52 * i
            col = BAD if n.startswith("semi") else SUPPLIER
            b = bar(-1.0, y, 6.0 * v / mx, 0.36, col)
            rows.add(VGroup(tx(n, 16, BAD if col == BAD else WHITE).next_to([-1.15, y, 0], LEFT, buff=0.0), b,
                            tx(f"${v:.1f}bn", 15, col, bold=True).next_to(b, RIGHT, buff=0.12)))
        other = tx(f"and ${D['other']:.0f}bn of other materials and components not broken out, of ${D['materials_total']:.0f}bn in all",
                   15, GREY_A).move_to([0.6, -2.85, 0])
        head = tx("What America's car assemblers bought in 2022", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("US Census Bureau, 2022 Economic Census, materials consumed by kind, NAICS 336110 (delivered cost)", size=12)
        with self.voiceover(
            "What do they buy? The census asked the assembly plants. <bookmark mark='a'/> The biggest single item is metal "
            f"stampings, {mats[0][1]:.0f} billion dollars' worth: the panels and brackets other companies press. Then "
            "transmissions and the parts that carry power to the wheels, then engines, other parts, seats and interiors, "
            "electrical and electronic equipment, glass, plastics. <bookmark mark='b'/> Near the bottom, almost a "
            f"rounding error at {D['materials']['semiconductors and related devices']:.1f} billion dollars: semiconductors. "
            f"Remember that line. <bookmark mark='c'/> In all the plants bought {D['materials_total']:.0f} billion "
            "dollars of materials and parts that year. Every one of those suppliers wants a margin too, which is the "
            "squeeze a carmaker lives in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(rows, opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[:-1]],
                                  lag_ratio=0.25), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[-1][0]), GrowFromEdge(rows[-1][1], LEFT), FadeIn(rows[-1][2]))
            self.play(Indicate(rows[-1], color=BAD))
            vo.wait_until("c")
            self.play(FadeIn(other))
        self.clear_scene()
