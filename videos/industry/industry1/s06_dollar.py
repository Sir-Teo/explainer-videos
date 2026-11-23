from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 5, "Follow the dollar", "Where does each of the 1,099 dollars end up?",
             "Chapter five. Follow the dollar.", lit=("dollar",))
        self.column()
        self.check()

    def column(self):
        D = R["dollar17"]
        items = slices("dollar17", collapse_parts=True)
        notes = {"Shop or carrier": "60% of Apple's sales go through carriers and resellers",
                 "All the parts": "display, chip, cameras, radios, memory ...",
                 "Assembly and test": "Foxconn, Luxshare, Tata",
                 "Shipping, warranty, licences": "", "Apple: research and selling": "14.9% of Apple's revenue",
                 "Income tax": "15.6% of profit, Apple's 2025 rate", "Apple's profit": "what is left for its owners"}
        items = [(l, a, c, notes.get(l, n)) for l, a, c, n in items]
        col = viz.DollarColumn(items, height=6.0, width=1.7, label_x=0.9, size=22, label_width=6.0)
        col.shift(np.array([-2.0 - col.slices.get_center()[0], -0.25 - col.slices.get_center()[1], 0]))
        top = col.top_label(money(D["price"]), 34)
        gross = D["gross"]
        apple_cut = Rectangle(width=0.08, height=sum(s.height for s in col.slices[4:]), fill_color=I.BRAND,
                              fill_opacity=1, stroke_width=0).next_to(col.slices[4:], LEFT, buff=0.12)
        gl = VGroup(TB(money(gross), 26, I.BRAND), T("Apple's gross profit", 18, I.TEXT),
                    T(f"{pct(D['gross_margin'])} of the {money(D['revenue'])}", 16, I.DIM),
                    T("Apple receives", 16, I.DIM)).arrange(DOWN, buff=0.05).next_to(apple_cut, LEFT, buff=0.2)
        rng = T(f"profit range {money(D['profit_range'][0])} to {money(D['profit_range'][1])}", 18, I.PROFIT)
        rng.next_to(col.labels[-1], DOWN, buff=0.1).align_to(col.labels[-1], LEFT)
        tag = estimate_tag("estimate: our model; ranges in the Register", corner=UR)
        src = source("Apple 10-K FY2025-26; TrendForce; WSJ; our assumptions", corner=DL)
        hand = draw.coin_stack(14, 0.17).move_to([-6.0, 3.15, 0])
        hand_t = T("what you pay", 18, I.DIM).next_to(hand, DOWN, buff=0.12)

        flying = []

        def land():
            self.remove(*flying)
            flying.clear()

        def k(i, n=4):
            coins, fly = draw.coin_flow(hand.get_top(), col.slices[i].get_center(), n=n, r=0.09, arc=-0.5)
            self.add(coins)
            flying.append(coins)
            return AnimationGroup(fly, GrowFromEdge(col.slices[i], DOWN), Create(col.leaders[i]), FadeIn(col.labels[i]))
        with self.voiceover(
            "Now follow the 1,099 dollars, starting where you hand it over. <bookmark mark='a'/> Six in every ten "
            "iPhones, by value, are sold through carriers and other resellers, Apple's annual report says; the rest "
            "through Apple's own stores and website. A carrier keeps a margin on the phones it sells, often a thin "
            "one, because it earns its money on your monthly plan. Averaged over all sales, we estimate the shop "
            "keeps about 66 dollars. <bookmark mark='b'/> That leaves Apple about 1,033. Out of it Apple pays for "
            "the parts, 520 dollars, <bookmark mark='c'/> and about 30 for assembly and testing, <bookmark "
            "mark='d'/> and about 40 more for shipping, warranty repairs and patent licences. <bookmark mark='e'/> "
            "What remains is Apple's gross profit on the phone: about 443 dollars, or 43 percent of what Apple "
            "receives. That is above the 37 percent Apple reports for all its products together, as you would "
            "expect for its most expensive phone. <bookmark mark='f'/> From that, Apple pays for its research, "
            "design, marketing and stores. Across the company these cost about 15 cents of every dollar of sales, "
            "so about 154 dollars on this phone. <bookmark mark='g'/> Income tax takes about 45. <bookmark "
            "mark='h'/> And Apple's profit, after everything, is about 244 dollars. Because several steps are "
            "estimates, the true figure could be anywhere from about 150 to about 360."
        ) as vo:
            self.play(FadeIn(top), FadeIn(src), FadeIn(tag), FadeIn(hand, shift=DOWN * 0.2), FadeIn(hand_t))
            vo.wait_until("a")
            self.play(k(0))
            land()
            vo.wait_until("b")
            self.play(k(1), run_time=1.4)
            land()
            vo.wait_until("c")
            self.play(k(2))
            land()
            vo.wait_until("d")
            self.play(k(3))
            land()
            vo.wait_until("e")
            for i in range(4, 7):
                col.slices[i].set_opacity(0.25)
            self.play(*[k(i, 2) for i in range(4, 7)], FadeIn(apple_cut), FadeIn(gl), run_time=1.4)
            land()
            for i in range(4, 7):
                self.remove(col.labels[i], col.leaders[i])
            vo.wait_until("f")
            self.play(col.slices[4].animate.set_opacity(0.9), FadeIn(col.labels[4]), Create(col.leaders[4]))
            vo.wait_until("g")
            self.play(col.slices[5].animate.set_opacity(0.9), FadeIn(col.labels[5]), Create(col.leaders[5]))
            vo.wait_until("h")
            self.play(col.slices[6].animate.set_opacity(0.9), FadeIn(col.labels[6]), Create(col.leaders[6]),
                      FadeIn(rng))
        self.clear_scene()

    def check(self):
        D = R["dollar17"]
        price = D["price"]
        piles = [("The shop or the carrier", amount("channel"), I.CHANNEL),
                 ("All the parts", D["bom"], COL["parts"]),
                 ("The factory that assembles it", amount("assembly"), I.ASSEMBLY),
                 ("Apple: research, design, selling", amount("opex"), I.BRAND),
                 ("Apple's profit, after tax", amount("profit"), I.PROFIT)]
        rows = VGroup()
        for name, a, c in piles:
            rows.add(VGroup(T(name, 25, I.TEXT), TB(money(a), 30, c),
                            T(f"{100 * a / price:.0f} cents of each dollar", 22, I.DIM)))
        for i, r in enumerate(rows):
            y = 2.1 - 0.66 * i
            r[0].move_to(np.array([-0.4, y, 0]), aligned_edge=RIGHT)
            r[1].move_to(np.array([0.0, y, 0]), aligned_edge=LEFT)
            r[2].move_to(np.array([1.9, y, 0]), aligned_edge=LEFT)
        rest = T(f"plus {money(amount('other_cogs'))} shipping, warranty and licences, and {money(amount('tax'))} "
                 "income tax", 20, I.DIM).next_to(rows, DOWN, buff=0.4)
        head = TB("Your guess, checked", 30, I.ACCENT).to_edge(UP, buff=0.6)
        apple = VGroup(T("Apple as a whole, fiscal 2026:", 22, I.DIM),
                       TB(f"{money_short(R_ap['ni'])} profit on {money_short(R_ap['rev'])} of sales", 22, I.TEXT),
                       T("= 28 cents of each dollar. This phone: 24 cents of each dollar Apple receives.", 22,
                         I.DIM)).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now check your guess. <bookmark mark='a'/> The shop or carrier: about 66 dollars, six cents of each "
            "dollar. All the parts: 520, 47 cents. The factory that assembles it: about 30 dollars, less than three "
            "cents. Apple's research, design and selling: about 154, 14 cents. And Apple's profit: about 244 "
            "dollars, 22 cents of each dollar you paid. <bookmark mark='b'/> The factory gets the least of all the "
            "piles, and the company that designed the phone and owns the brand keeps the most. <bookmark mark='c'/> "
            "Is 244 dollars plausible? Apple's own accounts say yes. In fiscal 2026 the company as a whole made 132 "
            "billion dollars of profit on 479 billion of sales: 28 cents of each dollar. Our phone gives 24."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.55), run_time=5)
            self.play(FadeIn(rest))
            vo.wait_until("b")
            self.play(Indicate(rows[2], color=I.ASSEMBLY), Indicate(rows[4], color=I.PROFIT))
            vo.wait_until("c")
            self.play(FadeIn(apple, shift=UP * 0.1))
        self.clear_scene()


R_ap = {"ni": get("apple.net_income.fy2026"), "rev": get("apple.revenue.fy2026")}
