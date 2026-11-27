from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Bottler(VoiceoverScene):
    def construct(self):
        card(self, 5, "Concentrate and bottlers", "Why does Coca-Cola leave the bottling to others?",
             "Chapter five. Concentrate and bottlers. Coca-Cola's drinks are sold in more than two hundred countries and "
             "territories, and it fills few of the bottles itself. The arrangement splits the brand from the heavy "
             "work of making and delivering.", lit=("make", "dollar"))
        self.system()
        self.split()
        self.margins()
        self.daily()

    def system(self):
        B = R["bottler"]
        vat = VGroup(RoundedRectangle(corner_radius=0.1, width=1.2, height=1.4, stroke_width=0, fill_color="#5A2A1A", fill_opacity=1),
                     tx("concentrate", 14, WHITE, bold=True)).move_to([-5.0, 0.6, 0])
        vat[1].move_to(vat[0])
        plant = draw.factory(1.8, DRINK).move_to([-1.4, 0.6, 0])
        cans = VGroup(*[draw.can(0.55) for _ in range(6)]).arrange(RIGHT, buff=0.12).move_to([2.6, 0.6, 0])
        shop = draw.shop(1.2).move_to([5.6, 0.6, 0])
        a1 = Arrow(vat.get_right(), plant.get_left(), buff=0.2, color=GREY_B)
        a2 = Arrow(plant.get_right(), cans.get_left(), buff=0.2, color=GREY_B)
        a3 = Arrow(cans.get_right(), shop.get_left(), buff=0.2, color=GREY_B)
        l1 = tx("Coca-Cola: the formula, the brand, the advertising", 15, BAD, bold=True).move_to([-3.6, -0.5, 0])
        l2 = tx("the bottler: water, sugar, cans, trucks, salespeople", 15, DRINK, bold=True).move_to([1.4, -1.1, 0])
        n = tx(f"{B['cases']:.1f} billion unit cases in 2025: 24 servings of 8 ounces each", 18, WHITE, bold=True).move_to([0, -2.2, 0])
        src = source("The Coca-Cola Company, Form 10-K 2025", size=12)
        beat(self,
             "The Coca-Cola system has two halves. <bookmark mark='a'/> Coca-Cola makes concentrate, the syrup base that "
             "carries the formula, and owns the brand and its advertising. <bookmark mark='b'/> Bottling companies, most of "
             "them independent, buy the concentrate, add water and sweetener, fill the bottles and cans, <bookmark mark='c'/> "
             "and deliver them to shops and restaurants. <bookmark mark='d'/> Together they sold "
             f"{B['cases']:.1f} billion unit cases in 2025, a unit case being twenty-four servings of eight ounces.",
             base=[src], steps=[[vat, l1], [a1, plant, l2], [a2, cans, a3, shop], n])

    def split(self):
        B = R["bottler"]
        vol = viz.bar_split([("concentrate", B["conc_vol"], BAD), ("finished", 100 - B["conc_vol"], DRINK)], 100, width=9.0, height=0.7).move_to([0.8, 1.2, 0])
        rev = viz.bar_split([("concentrate", B["conc_rev"], BAD), ("finished", 100 - B["conc_rev"], DRINK)], 100, width=9.0, height=0.7).move_to([0.8, -0.6, 0])
        vl = tx("share of the cases sold", 16, WHITE, bold=True).next_to(vol, LEFT, buff=0.3)
        rl = tx("share of Coca-Cola's revenue", 16, WHITE, bold=True).next_to(rev, LEFT, buff=0.3)
        for g in (vl, rl):
            if g.get_left()[0] < -7.0:
                g.shift(RIGHT * (-7.0 - g.get_left()[0]))
        n1 = VGroup(tx(f"{B['conc_vol']}%", 20, "#0E1117", bold=True).move_to(vol[0]), tx(f"{100 - B['conc_vol']}%", 20, "#0E1117", bold=True).move_to(vol[1]))
        n2 = VGroup(tx(f"{B['conc_rev']}%", 20, "#0E1117", bold=True).move_to(rev[0]), tx(f"{100 - B['conc_rev']}%", 20, "#0E1117", bold=True).move_to(rev[1]))
        key = VGroup(tx("concentrate sold to bottlers", 15, BAD, bold=True), tx("finished drinks it makes itself", 15, DRINK, bold=True)).arrange(RIGHT, buff=0.8).move_to([0.8, -2.0, 0])
        src = source("The Coca-Cola Company, Form 10-K 2025: concentrate and finished product operations", size=12)
        beat(self,
             "Coca-Cola does run some bottlers itself. <bookmark mark='a'/> Of the cases sold in 2025, "
             f"{B['conc_vol']} per cent came from concentrate it sold to bottlers, and {100 - B['conc_vol']} per cent from "
             f"finished drinks it made and sold itself. <bookmark mark='b'/> But the finished drinks brought it "
             f"{100 - B['conc_rev']} per cent of its revenue: a case it bottles brings in far more money than a case of concentrate. Its own report "
             "says finished drinks bring more revenue but lower gross margins than concentrate. So where it can, Coca-Cola "
             "sells the syrup and lets others fill the bottles.",
             base=[key, src], steps=[[vol, vl, n1], [rev, rl, n2]])

    def daily(self):
        E = R["extra"]
        B = R["bottler"]
        cans = VGroup(*[draw.can(0.42, color=BAD) for _ in range(22)]).arrange_in_grid(2, 11, buff=0.14).move_to([0, 0.9, 0])
        n = tx(f"about {E['servings_day'] / 1e9:.1f} billion servings a day", 30, BAD, bold=True).move_to([0, -1.0, 0])
        how = tx(f"{B['cases']:.1f} billion unit cases a year x 24 servings / 365 days", 16, GREY_A).move_to([0, -1.8, 0])
        tag = estimate_tag("this series' arithmetic from the Coca-Cola Company's Form 10-K 2025", size=12)
        beat(self,
             "Scale makes the arrangement work. <bookmark mark='a'/> Thirty-three point eight billion unit cases, each "
             "twenty-four servings, spread over a year, <bookmark mark='b'/> is about "
             f"{E['servings_day'] / 1e9:.1f} billion servings of the system's drinks every day. <bookmark mark='c'/> Coca-Cola's "
             f"net profit works out at about {E['profit_serving']:.1f} cents a serving. Small on each one; multiplied by "
             "billions a day, it pays for the advertising that keeps the name in every one of those countries, and leaves "
             "thirteen billion dollars a year over.",
             base=[tag], steps=[cans, n, how])

    def margins(self):
        B = R["bottler"]
        items = [("Coca-Cola: gross margin", B["ko_gm"], BAD, f"{100 * B['ko_gm']:.0f}%"),
                 ("Coca-Cola Consolidated: gross margin", B["coke_gm"], DRINK, f"{100 * B['coke_gm']:.0f}%"),
                 ("Coca-Cola: net margin", B["ko_margin"], BAD, f"{100 * B['ko_margin']:.0f}%"),
                 ("Coca-Cola Consolidated: net margin", B["coke_margin"], DRINK, f"{100 * B['coke_margin']:.0f}%")]
        rows = hbars(items, max_value=0.7, x0=0.2, top=1.4, row=0.85, length=5.6, size=17, bar_h=0.45)
        src = source("The Coca-Cola Company and Coca-Cola Consolidated, Inc., Forms 10-K 2025 via SEC company facts", size=12)
        beat(self,
             "Compare the two halves in 2025. <bookmark mark='a'/> Coca-Cola kept "
             f"{100 * B['ko_gm']:.0f} cents of each dollar after the cost of what it sold, <bookmark mark='b'/> Coca-Cola "
             f"Consolidated, an American bottler, {100 * B['coke_gm']:.0f}. <bookmark mark='c'/> After everything, "
             f"Coca-Cola's net profit was {100 * B['ko_margin']:.0f} cents of each dollar, <bookmark mark='d'/> the bottler's "
             f"{100 * B['coke_margin']:.0f}. The brand owner keeps the part of the business that is the formula and the "
             "brand; the trucks, factories and salespeople, and their thinner margins, belong to someone else.",
             base=[rows.axis, src], steps=list(rows))
