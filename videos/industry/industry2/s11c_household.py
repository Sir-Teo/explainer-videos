from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

# The groups both columns use, so a slice can be followed from "as bought" to "as earned"
GROUPS = [("Housing and finance", ["Finance and real estate"], "#F2C14E"),
          ("Health and education", ["Education and health"], "#7BD88F"),
          ("Shops and wholesalers", ["Retail", "Wholesale"], "#7EC8F5"),
          ("Goods and energy", ["Manufacturing", "Farms", "Mining", "Utilities", "Construction"], "#F2A65A"),
          ("Restaurants, hotels, fun", ["Leisure and hotels"], "#4FD1C5"),
          ("Business services", ["Business services"], "#B58CFF"),
          ("Everything else", ["Information", "Transport", "Other services", "Government"], "#8B95A7")]
IMPORTS = ("Made abroad", I.COST)


def grouped(d, names):
    by = dict(zip(names, d))
    return [sum(by[k] for k in ks) for _, ks, _ in GROUPS]


class Household(VoiceoverScene):
    def construct(self):
        card(self, 12, "A household's dollar, followed back", "When a family spends a dollar, who ends up with it?",
             "Chapter twelve. A household's dollar, followed back.", lit=("dollar",))
        self.dollar()
        self.three()

    def column(self, vals, x=-4.6, width=1.5, height=5.6, bottom=-3.05):
        g = VGroup()
        y = bottom + height  # stacked from the top, in the table's order
        tot = sum(vals)
        for v, col in zip(vals, [c for _, _, c in GROUPS] + [IMPORTS[1]]):
            h = max(height * v / tot, 0.004)
            g.add(Rectangle(width=width, height=h, fill_color=col, fill_opacity=0.92, stroke_color=BACKGROUND,
                            stroke_width=1.2).move_to(np.array([x, y - h / 2, 0])))
            y -= h
        return g

    def dollar(self):
        H = R["household"]
        P = H["pce"]
        bought = grouped(P["bought"], H["names"]) + [0.0]
        earned = grouped(P["va"], H["names"]) + [P["imports"] + P["other"]]
        col = self.column(bought)
        names = [n for n, _, _ in GROUPS] + [IMPORTS[0]]
        cols = [c for _, _, c in GROUPS] + [IMPORTS[1]]
        ys = [1.95 - k * 0.6 for k in range(len(names))]
        table = VGroup()
        for n, c, y, b, e in zip(names, cols, ys, bought, earned):
            chip = Square(0.24, fill_color=c, fill_opacity=0.95, stroke_width=0).move_to(np.array([-2.75, y, 0]))
            nm = T(n, 21, I.TEXT).next_to(chip, RIGHT, buff=0.18)
            bt = TB(f"{100 * b:.0f}¢" if b > 0 else "—", 23, I.TEXT).move_to(np.array([2.95, y, 0]))
            et = TB(f"{100 * e:.0f}¢", 23, c).move_to(np.array([4.95, y, 0]))
            table.add(VGroup(chip, nm, bt, et))
        hb = T("as bought", 20, I.DIM).move_to(np.array([2.95, 2.62, 0]))
        he = T("as earned", 20, I.DIM).move_to(np.array([4.95, 2.62, 0]))
        top = TB("$1", 30, I.MONEY).next_to(col, UP, buff=0.12)
        head = T("One dollar of American households' spending, 2023, followed back through the table", 22,
                 I.TEXT).to_edge(UP, buff=0.3)
        src = source("Computed: BEA 2023 use table; imports assumed the same share of each commodity for every user",
                     corner=DR, size=13)
        k_bus, k_imp, k_goods, k_health = 5, 7, 3, 1
        with self.voiceover(
            "Now Part one's device, the Dollar, for the whole economy. Take one dollar that an American household "
            "spends, and follow it back through Leontief's table to everyone who earns a piece of it. <bookmark "
            f"mark='a'/> First, what the dollar buys. {100 * bought[0]:.0f} cents goes on housing and finance, most "
            f"of it rent; {100 * bought[1]:.0f} on health care and education; {100 * bought[2]:.0f} to the shops and "
            f"wholesalers for the service of selling; {100 * bought[3]:.0f} on goods and energy at the factory gate; "
            f"{100 * bought[4]:.0f} in restaurants, hotels and places of fun; and two cents on the services that "
            "businesses sell, such as advertising, law and software. <bookmark mark='b'/> Now follow every cent "
            "back, through every supplier, round after round, to the wages and profits of the people who made it. "
            f"<bookmark mark='c'/> Health and education keep {100 * earned[1]:.0f} of their {100 * bought[1]:.0f} "
            "cents; the rest pays for medicines, equipment and the services they buy. Goods and energy keep about "
            f"{100 * earned[3]:.0f} of {100 * bought[3]:.0f}. <bookmark mark='d'/> The biggest surprise is "
            f"business services. Households hardly buy them, two cents, yet {100 * earned[5]:.0f} cents of the "
            "dollar ends up there: the lawyers, accountants, advertisers, software houses, cleaners and temporary "
            "staff that every other business hires. <bookmark mark='e'/> And about ten cents leaves the country, "
            "as imported goods and the imported parts inside American ones. What you buy and who you pay are not "
            "the same thing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in col[:-1]], lag_ratio=0.15), FadeIn(top),
                      FadeIn(hb), LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[2])) for r in table[:-1]],
                                              lag_ratio=0.15), run_time=3.2)
            vo.wait_until("b")
            self.play(Transform(col, self.column(earned)), FadeIn(he), FadeIn(VGroup(*[r[3] for r in table[:-1]])),
                      FadeIn(VGroup(table[-1][0], table[-1][1], table[-1][2])), run_time=2.5)
            self.play(FadeIn(table[-1][3]))
            vo.wait_until("c")
            self.play(Indicate(table[k_health], color="#7BD88F", scale_factor=1.04))
            self.play(Indicate(table[k_goods], color="#F2A65A", scale_factor=1.04))
            vo.wait_until("d")
            self.play(Indicate(table[k_bus], color="#B58CFF", scale_factor=1.08), Indicate(col[k_bus], color=WHITE))
            vo.wait_until("e")
            self.play(Indicate(table[k_imp], color=I.COST, scale_factor=1.08), Indicate(col[k_imp], color=WHITE))
        self.clear_scene()

    def three(self):
        H = R["household"]
        rows = VGroup()
        W = 8.4
        spec = [("A household's dollar", "pce"), ("A dollar of investment", "investment"),
                ("A government's dollar", "government")]
        tops = {}
        for k, (label, key) in enumerate(spec):
            d = H[key]
            dom = sum(d["va"])
            imp = d["imports"] + d["other"]
            y = 1.3 - k * 1.55
            name = TB(label, 22, I.TEXT).move_to(np.array([-6.3, y + 0.5, 0]), aligned_edge=LEFT)
            a = Rectangle(width=W * dom, height=0.5, fill_color=I.PROFIT, fill_opacity=0.85, stroke_width=0)
            b = Rectangle(width=W * imp, height=0.5, fill_color=I.COST, fill_opacity=0.9, stroke_width=0)
            bar = VGroup(a, b).arrange(RIGHT, buff=0).move_to(np.array([-6.3, y - 0.05, 0]), aligned_edge=LEFT)
            ta = T(f"{100 * dom:.0f}¢ to American industries", 17, "#0E1117").move_to(a)
            tb = TB(f"{100 * imp:.0f}¢ abroad", 18, I.COST).next_to(b, RIGHT, buff=0.12)
            j = int(np.argmax(d["va"]))
            best = T(f"largest share: {H['names'][j].lower()}, {100 * d['va'][j]:.0f}¢", 17, I.DIM).next_to(
                bar, DOWN, buff=0.1).align_to(bar, LEFT)
            tops[key] = (H["names"][j], d["va"][j], imp)
            rows.add(VGroup(name, bar, ta, tb, best))
        head = T("Three buyers' dollars, 2023: how much stays in the country", 24, I.TEXT).to_edge(UP, buff=0.35)
        src = source("Computed: BEA 2023 use table", corner=DR, size=13)
        inv_imp = tops["investment"][2]
        with self.voiceover(
            "Do the same for the other buyers. <bookmark mark='a'/> Of a household's dollar, about 90 cents stays "
            "with American industries. <bookmark mark='b'/> Of a dollar of business investment, only about "
            f"{100 * (1 - inv_imp):.0f}: {100 * inv_imp:.0f} cents leaves the country, because so much investment is "
            "machinery, computers and equipment made abroad, and the largest single share goes to business "
            "services, the software and research that count as investment. <bookmark mark='c'/> Of a government's "
            "dollar, more than 90 cents stays at home, almost half of it as the pay of the government's own "
            "employees. <bookmark mark='d'/> These are the sums behind the arguments about where money should be "
            "spent: the same dollar supports very different industries, and very different numbers of jobs, "
            "depending on who spends it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                r = rows[i]
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), FadeIn(r[3]), FadeIn(r[4]))
            vo.wait_until("d")
            self.play(Indicate(rows[1][3], color=I.COST, scale_factor=1.1))
        self.clear_scene()
        assert tops["investment"][0] == "Business services" and tops["government"][0] == "Government"
