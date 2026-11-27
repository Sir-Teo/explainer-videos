from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Ads(VoiceoverScene):
    def construct(self):
        card(self, 3, "Advertising", "Why does the biggest advertiser stay the biggest?",
             "Chapter three. Advertising. A brand's premium is paid for with advertising. And advertising, it turns out, "
             "favours the biggest spender. The economics of a television campaign are the economics of a "
             "factory: a large fixed cost, spread over every unit sold.", lit=("moat",))
        self.pg()
        self.memory()
        self.share()
        self.scale()
        self.name()

    def pg(self):
        A = R["ads"]
        items = [(str(y)[2:], v, ADS, f"${v:.1f}bn") for y, v in sorted(A["pg"].items())]
        bars_ = vbars(items, base_y=-2.3, height=3.6, width=0.8, gap=0.35, size=14)
        tv = VGroup(RoundedRectangle(corner_radius=0.08, width=1.3, height=0.9, stroke_color=GREY_A, stroke_width=3, fill_color="#1A2230", fill_opacity=1),
                    draw.detergent(0.6)).move_to([-5.6, 2.2, 0])
        tv[1].move_to(tv[0])
        lab = tx("P&G's advertising, fiscal years", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("The Procter & Gamble Company, Forms 10-K for fiscal 2020 to 2026: advertising costs", size=12)
        sh = A["pg_share"]
        beat(self,
             "Procter and Gamble spends heavily to be remembered. <bookmark mark='a'/> It spent "
             f"{A['pg'][2018]:.1f} billion dollars on television, print, radio, digital and in-store advertising in fiscal "
             f"2018, <bookmark mark='b'/> and {A['pg'][2026]:.1f} billion in fiscal 2026, about {100 * sh[2026]:.0f} cents of "
             f"every dollar of sales, and {100 * (A['pg'][2026] / A['pg'][2025] - 1):.0f} per cent more than the year before. "
             "Sales grew by three per cent that year; the advertising grew faster.",
             base=[tv, lab, src], steps=[VGroup(*bars_[:4]), VGroup(*bars_[4:])])

    def memory(self):
        U = R["run"]
        cut = U["choices"]["cut"]["rows"]
        stock = {0: U["ads"] / U["decay"]}
        stock.update({r["year"]: r["stock"] for r in cut})
        ch = line_chart({"memory": (stock, ADS)}, x=(0, 8), y=(0, 550), xticks=list(range(0, 9)), yticks=[0, 100, 200, 300, 400, 500],
                        xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{v:.0f}", ylabel="the stock of advertising people remember (the Works, $m of past spending)",
                        width=8.6, height=4.2, center=(-0.8, -0.5), label_end=False)
        m0 = marker(ch.ax, 0, stock[0], f"steady: {stock[0]:.0f}", ADS, side=RIGHT)
        m8 = marker(ch.ax, 8, stock[8], f"year 8: {stock[8]:.0f}", BAD, side=UP)
        tag = estimate_tag(f"the Works: {100 * U['decay']:.0f}% of the stock wears off each year", size=12)
        beat(self,
             "Why keep spending? Because advertising works like a stock that leaks. <bookmark mark='a'/> In the Works' "
             f"brand, {U['ads']:.0f} million dollars a year keeps a stock of about {stock[0]:.0f} million dollars' worth of "
             "past advertising in shoppers' minds, topped up as fast as it wears off. <bookmark mark='b'/> Stop, and a fifth "
             f"of it leaks away each year: by year eight, {stock[8]:.0f}. That is why the leaders never stop: the brand is "
             "the memory, and the memory must be refilled.",
             base=[ch.frame, tag], steps=[m0, [ch.lines["memory"], m8]])

    def share(self):
        A = R["ads"]["share"]
        items = [(k, v, ADS if v >= 0.08 else GREY_B, f"{100 * v:.1f}%") for k, v in sorted(A.items(), key=lambda kv: -kv[1])]
        rows = hbars(items, max_value=0.15, x0=-0.4, top=2.5, row=0.36, length=6.2, size=14, bar_h=0.24)
        lab = tx("advertising as a share of sales, latest fiscal year", 15, GREY_A).to_edge(UP, buff=0.55)
        src = source("Forms 10-K via SEC company facts: advertising expense over revenue", size=12)
        beat(self,
             "Across the industry, advertising takes from three to thirteen cents of each dollar. <bookmark mark='a'/> Colgate "
             f"spent {100 * A['Colgate-Palmolive']:.0f} per cent of its sales on advertising, P&G and Church and Dwight about "
             f"{100 * A['Church & Dwight']:.0f}, Coca-Cola {100 * A['Coca-Cola']:.0f}. <bookmark mark='b'/> PepsiCo, much of "
             f"whose sales are snacks and bottling, {100 * A['PepsiCo']:.1f}; and Philip Morris International, "
             f"{100 * A['Philip Morris International']:.1f}: a cigarette maker can spend little on advertising and still "
             "keep among the highest margins in this film, for reasons chapter seven comes to.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:6]), VGroup(*rows[6:])])

    def name(self):
        B = R["bottler"]
        cans = VGroup(*[draw.can(0.5, color=BAD if i < round(B["coke_share"] / 10) else GREY_B) for i in range(10)]).arrange(RIGHT, buff=0.18).move_to([0, 0.6, 0])
        t = tx(f"Trademark Coca-Cola: {B['coke_share']}% of the system's {B['cases']:.1f} billion unit cases", 20, BAD, bold=True).move_to([0, -1.2, 0])
        src = source("The Coca-Cola Company, Form 10-K 2025", size=12)
        beat(self,
             "And a name, once built, carries a whole company. <bookmark mark='a'/> Coca-Cola sells waters, juices, teas, coffees and sports drinks, but "
             f"<bookmark mark='b'/> the drinks carrying the Coca-Cola name itself made up {B['coke_share']} per cent of all "
             f"the {B['cases']:.1f} billion cases its system sold in 2025: almost half of everything, under one name.",
             base=[src], steps=[cans, t])

    def scale(self):
        H = R["hook"]
        comp = {c["name"]: c for c in R["landscape"]["companies"]}
        items = [("P&G's advertising alone", H["ads"], ADS, f"${H['ads']:.1f}bn"),
                 ("all of Clorox's sales", comp["Clorox"]["rev"], STORE, f"${comp['Clorox']['rev']:.1f}bn"),
                 ("all of Church & Dwight's sales", comp["Church & Dwight"]["rev"], STORE, f"${comp['Church & Dwight']['rev']:.1f}bn")]
        rows = hbars(items, max_value=11, x0=-0.4, top=1.2, row=1.0, length=6.2, size=18, bar_h=0.5)
        note = tx("A fixed cost a newcomer cannot spread", 20, PRICE, bold=True).move_to([0, -2.0, 0])
        src = source("Forms 10-K: P&G advertising costs (fiscal 2026); Clorox (fiscal 2025) and Church & Dwight (2025) revenue via "
                     "SEC company facts", size=12)
        beat(self,
             "And scale is the point. <bookmark mark='a'/> P&G's advertising budget alone, "
             f"{H['ads']:.1f} billion dollars, <bookmark mark='b'/> is larger than the entire sales of Clorox, "
             f"{comp['Clorox']['rev']:.1f} billion, <bookmark mark='c'/> or of Church and Dwight, "
             f"{comp['Church & Dwight']['rev']:.1f} billion. A television campaign costs the same whether it sells a "
             "million bottles or a hundred million, so the brand that sells the most pays the least per bottle to be "
             "remembered. <bookmark mark='d'/> Advertising is a fixed cost, and fixed costs favour the biggest. A challenger "
             "must spend as much as the leader to be remembered as well, on a fraction of the sales.",
             base=[rows.axis, src], steps=[rows[0], rows[1], rows[2], note])
