from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

GUCCI = "#7BD88F"


class Houses(VoiceoverScene):
    def construct(self):
        card(self, 8, "The houses, and how fast taste turns", "Can a luxury name lose its pull?",
             "Chapter eight. The houses. Scarcity only works while people want the thing that is scarce, and taste can "
             "turn faster than a workshop can be built.", lit=("moat", "change"))
        self.gucci()
        self.profit()
        self.retail()
        self.ladder()
        self.deals()

    def gucci(self):
        G, H = R["fickle"]["gucci"], R["luxury"]["rms"]
        ch = line_chart({"Hermès": ({y: v / 1e3 for y, (v, o) in H.items()}, LUX),
                         "Gucci": ({y: v / 1e3 for y, (v, o) in G.items()}, GUCCI)},
                        x=(2022, 2025), y=(4, 18), xticks=[2022, 2023, 2024, 2025], yticks=[4, 6, 8, 10, 12, 14, 16, 18],
                        yfmt=lambda v: f"€{v:.0f}bn", ylabel="revenue", width=9.0, height=4.4, center=(-0.6, -0.45))
        src = source("Kering, full-year results 2023 and 2025; Hermès International, full-year results 2023 to 2025", size=12)
        beat(self,
             "Two houses, four years. <bookmark mark='a'/> In 2022 Hermès's revenue was "
             f"{H[2022][0] / 1e3:.1f} billion euros, and it has grown every year since, to {H[2025][0] / 1e3:.1f}. "
             f"<bookmark mark='b'/> In 2022 Gucci, the largest brand of the French group Kering, was not far behind, at "
             f"{G[2022][0] / 1e3:.1f} billion. Then it fell: {G[2023][0] / 1e3:.1f} billion in 2023, {G[2024][0] / 1e3:.1f} "
             f"in 2024, {G[2025][0] / 1e3:.1f} in 2025. In three years Gucci lost more than two fifths of its sales, "
             "in the same market in which Hermès grew by more than a third.",
             base=[ch.frame, src], steps=[[ch.lines["Hermès"], ch.labels["Hermès"]], [ch.lines["Gucci"], ch.labels["Gucci"]]])

    def profit(self):
        G = R["fickle"]["gucci"]
        items = [(str(y), o / 1e3, GUCCI if y == 2022 else BAD, f"€{o / 1e3:.2f}bn") for y, (v, o) in G.items()]
        bars_ = vbars(items, base_y=-2.4, height=3.8, width=1.2, gap=0.7, size=18, max_value=4)
        lab = tx("Gucci's recurring operating income", 16, GREY_A).to_edge(UP, buff=0.7)
        src = source("Kering, full-year results 2023 and 2025", size=12)
        beat(self,
             f"And the profit fell faster than the sales. <bookmark mark='a'/> Gucci earned {G[2022][1] / 1e3:.1f} billion "
             f"euros of operating profit in 2022, <bookmark mark='b'/> {G[2023][1] / 1e3:.1f} in 2023, "
             f"<bookmark mark='c'/> {G[2024][1] / 1e3:.1f} in 2024 <bookmark mark='d'/> and {G[2025][1] / 1e3:.2f} in 2025: "
             f"a margin of {R['fickle']['gucci_margin']} per cent, down from more than a third. A luxury house's costs are "
             "mostly its shops, its staff, its shows and its advertising, and they do not shrink as fast as its sales.",
             base=[lab, src], steps=[bars_[0], bars_[1], bars_[2], bars_[3]])

    def retail(self):
        F = R["fickle"]
        shop = draw.shop(2.2) if hasattr(draw, "shop") else Square(1.6)
        shop.move_to([-3.6, 0.6, 0])
        c = VGroup(tx(f"{F['gucci_retail']:.0f}%", 54, GUCCI, bold=True), tx("of Gucci's 2025 revenue came from its own shops", 17, GREY_A)
                   ).arrange(DOWN, buff=0.1).move_to([2.6, 0.9, 0])
        note = tx("own shops: no wholesale buyer to absorb the stock, and no sale to clear it", 18, WHITE).move_to([0, -1.9, 0])
        src = source("Kering, 2025 full-year results", size=12)
        beat(self,
             "Why does a fall hurt a luxury house so much? <bookmark mark='a'/> Partly because it sells mostly in its own "
             f"shops: {F['gucci_retail']:.0f} per cent of Gucci's 2025 revenue. <bookmark mark='b'/> Our reading: a house "
             "that owns its shops controls its prices and its image, but it also pays the rent, the staff and the stock "
             "whether the shop is busy or not, and a sale would cheapen the very thing it sells. The rule that protects "
             "luxury on the way up is the one that hurts on the way down.",
             base=[shop, src], steps=[c, note])

    def ladder(self):
        F = R["fickle"]
        items = [("Coach", F["coach"][2024] / 1e3, F["coach"][2026] / 1e3), ("Kate Spade", F["kate"][0] / 1e3, F["kate"][1] / 1e3),
                 ("Michael Kors", F["mk"][0] / 1e3, F["mk"][1] / 1e3)]
        db = dumbbell(items, x=(0, 8), center=(1.0, -0.2), width=8.4, height=3.6, xticks=[0, 2, 4, 6, 8],
                      xfmt=lambda v: f"${v:.0f}bn", size=17)
        lab = tx("sales, fiscal 2024 to fiscal 2026", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Tapestry, Inc. and Capri Holdings Limited, Forms 10-K for fiscal 2026", size=12)
        c24, c26 = F["coach"][2024], F["coach"][2026]
        beat(self,
             "It happens lower down too, between brands sold side by side in the same malls. <bookmark mark='a'/> Coach's "
             f"sales rose from {c24 / 1e3:.1f} billion dollars in fiscal 2024 to {c26 / 1e3:.1f} billion in fiscal 2026, up "
             f"{100 * (c26 / c24 - 1):.0f} per cent, with its owner saying it was aiming at young shoppers just entering the "
             f"market. Over the same two years Kate Spade fell from {F['kate'][0] / 1e3:.2f} billion to "
             f"{F['kate'][1] / 1e3:.2f}, and Michael Kors from {F['mk'][0] / 1e3:.1f} to {F['mk'][1] / 1e3:.1f}. Coach and "
             "Kate Spade are even made in the same countries, mainly Vietnam, Cambodia and the Philippines. Same kind of "
             "bag, same kind of shop; different fortunes.",
             base=[lab, src], steps=[db])

    def deals(self):
        F = R["fickle"]
        rows = VGroup(tx("August 2023: Tapestry agrees to buy Capri (Michael Kors, Versace, Jimmy Choo)", 18, WHITE),
                      tx("November 2024: the agreement is terminated", 18, BAD),
                      tx(f"April 2025: Capri agrees to sell Versace to Prada for ${F['versace']:.3f}bn", 18, PRICE),
                      tx("December 2025: the sale is completed", 18, PRICE)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.4, 0])
        src = source("Tapestry, Inc., Form 10-K for fiscal 2026; Capri Holdings Limited, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "And names change hands. <bookmark mark='a'/> In August 2023 Tapestry, Coach's owner, agreed to buy Capri, the "
             "owner of Michael Kors, Versace and Jimmy Choo. <bookmark mark='b'/> In November 2024 the deal was called off. "
             f"<bookmark mark='c'/> In April 2025 Capri agreed to sell Versace to the Italian house Prada, for "
             f"{F['versace']:.3f} billion dollars, <bookmark mark='d'/> and the sale was completed that December. A "
             "luxury group is a portfolio of names, each one rising or falling with taste, and the groups buy and sell them "
             "the way an investor buys and sells shares.",
             base=[src], steps=[rows[0], rows[1], rows[2], rows[3]])
