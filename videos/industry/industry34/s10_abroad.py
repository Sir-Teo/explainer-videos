from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Abroad(VoiceoverScene):
    def construct(self):
        card(self, 8, "The world's franchisees", "How does an American brand run restaurants in a hundred countries?",
             "Chapter eight. The world's franchisees. Abroad, the big brands often franchise a whole country, or a whole "
             "region, to one company.", lit=("change",))
        self.systems()
        self.master()
        self.margins()
        self.map_()

    def systems(self):
        A = R["abroad"]
        items = [("Yum! Brands: KFC, Taco Bell, Pizza Hut, Habit", A["yum_units"], FR, f"{A['yum_units']:,}+"),
                 ("McDonald's", A["mcd_rest"], FR, f"{A['mcd_rest']:,}"),
                 ("Domino's", A["dpz_units"], FR, f"{A['dpz_units']:,}+")]
        rows = hbars(items, max_value=65000, x0=0.4, top=1.2, row=1.1, length=5.8, size=17, bar_h=0.55)
        hd = tx("Restaurants in each system, end of 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"{A['yum_fr']}% of Yum's restaurants are run by franchisees", 18, GREY_A).to_edge(DOWN, buff=0.85)
        src = source("Yum! Brands, McDonald's and Domino's, Forms 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Yum Brands, which owns KFC, Taco Bell and Pizza Hut, counted over {A['yum_units']:,} "
             f"restaurants in 155 countries and territories, {A['yum_fr']} per cent of them run by franchisees. "
             f"<bookmark mark='b'/> McDonald's, {A['mcd_rest']:,}. <bookmark mark='c'/> Domino's, more than "
             f"{A['dpz_units']:,} in over ninety markets. None of these companies could have built so many restaurants with "
             "its own money and managers.",
             base=[rows.axis, hd, note, src], steps=[rows[0], rows[1], rows[2]])

    def master(self):
        A = R["abroad"]
        c = stat_cards([(f"{A['arco_units']:,}", "McDonald's restaurants run by Arcos Dorados in Latin America", MASTER),
                        (f"{A['arco_roy']:.1f}%", "of their sales paid to McDonald's as royalty, rising to 6.5%", FR),
                        (f"${A['yumc_rev']:.1f}bn", "Yum China's revenue in 2025: KFC and Pizza Hut in China", MASTER)], y=0.4, size=34, span=12.6)
        src = source("Arcos Dorados, Form 20-F for 2025; Yum China, Form 10-K via SEC company facts", size=12)
        beat(self,
             "Abroad, whole regions go to master franchisees. <bookmark mark='a'/> Arcos Dorados, which calls itself the "
             f"world's largest independent McDonald's franchisee, ran {A['arco_units']:,} restaurants across Latin America at "
             f"the end of 2025. <bookmark mark='b'/> It pays McDonald's a royalty starting at {A['arco_roy']:.0f} per cent of "
             "sales, and runs some restaurants itself while sub-franchising others. <bookmark mark='c'/> In China, KFC and "
             f"Pizza Hut belong to Yum China, a separate listed company with {A['yumc_rev']:.1f} billion dollars of revenue in "
             f"2025, which pays Yum a licence fee of {get('ym34.china'):.0f} per cent of its sales. The brand stays American; "
             "the business becomes local.",
             base=[src], steps=[c[0], c[1], c[2]])

    def map_(self):
        mp = draw.world_map(12.0, lon=(-130, 150), lat=(-45, 60)).move_to([0, -0.2, 0])
        spots = [(-98, 38, "McDonald's, Yum, Domino's: home markets", FR, UP), (-55, -15, "Arcos Dorados: 21 countries and territories", MASTER, DOWN),
                 (110, 32, "Yum China: KFC and Pizza Hut", MASTER, DOWN), (78, 21, "Jubilant FoodWorks (India)", MASTER, DOWN),
                 (122, 13, "Jollibee (the Philippines)", OP, RIGHT)]
        dots = VGroup()
        for lon, lat, text, col, side in spots:
            d = Dot(mp.p(lon, lat), radius=0.12, color=col)
            dots.add(VGroup(d, tx(text, 14, col, bold=True).next_to(d, side, buff=0.12)))
        note = tx("Names only, not measured in this film: Jubilant FoodWorks and Jollibee", 13, GREY_B).to_edge(DOWN, buff=0.6)
        src = source("Arcos Dorados, Form 20-F; Yum China, Form 10-K", size=12)
        beat(self,
             "<bookmark mark='a'/> The American brands at home. <bookmark mark='b'/> Their great franchisees abroad: Arcos "
             "Dorados in Latin America, <bookmark mark='c'/> Yum China, <bookmark mark='d'/> and India's Jubilant FoodWorks. "
             "<bookmark mark='e'/> And local chains with brands of their own, like the Philippines' Jollibee, which this film "
             "names but has not measured.",
             base=[mp, note, src], steps=list(dots))

    def margins(self):
        C = {c["name"]: c for c in R["landscape"]["companies"]}
        names = ["McDonald's", "Yum! Brands", "Yum China", "Arcos Dorados"]
        cols = {"McDonald's": FR, "Yum! Brands": FR, "Yum China": MASTER, "Arcos Dorados": MASTER}
        items = [(n, 100 * C[n]["margin"], cols[n], f"{100 * C[n]['margin']:.1f}c") for n in names]
        rows = hbars(items, max_value=35, x0=-0.4, top=1.6, row=0.95, length=6.2, size=17, bar_h=0.5)
        hd = tx("Net profit per dollar of revenue, median of five years", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Forms 10-K and 20-F via SEC company facts", size=12)
        beat(self,
             "Who does better: the brand or its biggest franchisees? <bookmark mark='a'/> McDonald's and Yum, which collect "
             f"fees, kept {100 * C[chr(77) + 'cDonald' + chr(39) + 's']['margin']:.0f} and {100 * C['Yum! Brands']['margin']:.0f} "
             f"cents of each dollar of revenue over five years. <bookmark mark='b'/> Yum China, which runs the restaurants and "
             f"pays the fee, {100 * C['Yum China']['margin']:.0f}. <bookmark mark='c'/> Arcos Dorados, "
             f"{100 * C['Arcos Dorados']['margin']:.0f}. The franchisee's revenue is bigger, because it counts every meal; the "
             "franchisor's slice is smaller and much richer.",
             base=[rows.axis, hd, src], steps=[VGroup(rows[0], rows[1]), rows[2], rows[3]])
