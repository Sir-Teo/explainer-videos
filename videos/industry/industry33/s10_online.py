from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Online(VoiceoverScene):
    def construct(self):
        card(self, 8, "The internet and the middleman", "Did the web cut out the distributor, or become one of its tools?",
             "Chapter eight. The internet and the middleman. Grainger, a large American industrial distributor, runs two "
             "businesses side by side: one built on people, one on websites.", lit=("change",))
        self.two()
        self.margins()
        self.reading()

    def two(self):
        O = R["online"]
        left = VGroup(tx("High-Touch Solutions", 21, IND, bold=True), draw.van(1.4, color=IND), draw.shelf(1.6, rows=3, n=4),
                      tx(f"about 2 million products; {O['stocked']:.1f}m stocked company-wide", 14, GREY_A),
                      tx("sales reps, branches, inventory managed on site", 14, GREY_A)).arrange(DOWN, buff=0.2).move_to([-3.4, 0.2, 0])
        right = VGroup(tx("Endless Assortment: Zoro and MonotaRO", 21, TECH, bold=True), draw.laptop(1.6),
                       tx(f"about {O['zoro']:.0f} million and {O['monotaro']:.0f} million products", 14, GREY_A),
                       tx("websites and catalogues, few salespeople", 14, GREY_A)).arrange(DOWN, buff=0.2).move_to([3.4, 0.2, 0])
        src = source("W.W. Grainger, Form 10-K for 2025", size=12)
        beat(self,
             "Grainger sells maintenance and repair supplies: gloves, fans, motors, safety gear. <bookmark mark='a'/> Its "
             "high-touch business serves large customers with complex needs through salespeople, branches and "
             "inventory it manages on their sites, from about two million products. <bookmark mark='b'/> Its endless "
             f"assortment business, Zoro in America and MonotaRO in Japan, sells online from about {O['zoro']:.0f} and "
             f"{O['monotaro']:.0f} million products, with few salespeople at all. If the internet were going to cut out the "
             "middleman, this is where it would show.",
             base=[src], steps=[left, right])

    def margins(self):
        O = R["online"]
        rows = [["2025", "sales", "kept after the goods", "operating profit per dollar"],
                ["High-Touch Solutions N.A.", f"${O['ht']['sales']:.1f}bn", f"{O['ht']['gm']:.1f}c", f"{O['ht']['om']:.1f}c"],
                ["Endless Assortment", f"${O['ea']['sales']:.1f}bn", f"{O['ea']['gm']:.1f}c", f"{O['ea']['om']:.1f}c"]]
        cols = [None, [IND, WHITE, TRADE, GOOD], [TECH, WHITE, TRADE, GOOD]]
        t = table(rows, col_x=[-6.4, -2.0, 0.2, 3.4], top=1.2, row_h=0.9, size=19, colors=cols)
        src = source("W.W. Grainger, Form 10-K for 2025: segment results", size=12)
        beat(self,
             f"<bookmark mark='a'/> The high-touch business sold {O['ht']['sales']:.0f} billion dollars in 2025, kept "
             f"{O['ht']['gm']:.0f} cents of each dollar after the goods, and earned {O['ht']['om']:.0f} cents of operating "
             f"profit. <bookmark mark='b'/> The online business sold {O['ea']['sales']:.1f} billion, kept {O['ea']['gm']:.0f} "
             f"cents and earned {O['ea']['om']:.1f}. It grew sixteen per cent in the year against two for the high-touch "
             "business, but it earns less on each dollar: in this series' reading, a buyer comparing prices on a screen pays "
             "less for the same glove than one whose rep keeps the stockroom full. And notice that the online business is "
             "still a distributor: it buys the goods, stores them and ships them. Only the salesperson has gone.",
             base=[t[0], src], steps=[t[1], t[2]])

    def reading(self):
        g = VGroup(tx("What the internet changed, and what it did not", 22, WHITE, bold=True),
                   tx("it moved the order onto a screen, and cut the cost of a quote", 18, TECH),
                   tx("it made prices easier to compare, and margins thinner online", 18, BAD),
                   tx("it did not move the stock, the credit or the truck: someone still holds and delivers", 18, IND),
                   tx("so the distributors became e-commerce companies, and the jobs stayed", 18, GOOD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "In this series' reading: <bookmark mark='a'/> the internet moved the order onto a screen. "
             "<bookmark mark='b'/> It made prices easier to compare, and thinned the margin where buyers compare. "
             "<bookmark mark='c'/> But it did not move the stock, the credit or the truck: someone still has to hold the "
             "goods and bring them tomorrow. <bookmark mark='d'/> So the distributors became online businesses themselves, "
             "and the six million wholesale jobs of the intermission stayed. Travel agents, whose product was information "
             "alone, were not so lucky; Part 35 tells their story.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
