from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: buy land for 2029",
             "Homes you sell in three years need land you secure today. Own it, or option it?",
             "Chapter one. Run it. You build houses. In the Works, a home takes three years from bare field to keys: "
             "approvals, roads, pipes, then the house. So the land for homes you will sell in 2029 has to be secured now, "
             "before you know what prices or mortgage rates will be.", lit=("make", "change"))
        self.setup_()
        self.dollar()
        self.states()
        self.compare()
        self.capital()
        self.sweep()

    def setup_(self):
        U = R["run"]
        lot = draw.plot_lot(2.2).move_to([-4.2, 1.6, 0])
        frame = draw.house_frame(1.8).move_to([0, 1.6, 0])
        house = draw.house(1.8, color="#F2D0A4").move_to([4.2, 1.6, 0])
        arrows = VGroup(Arrow([-2.8, 1.6, 0], [-1.2, 1.6, 0], buff=0, stroke_color=GREY_B, stroke_width=3),
                        Arrow([1.2, 1.6, 0], [2.8, 1.6, 0], buff=0, stroke_color=GREY_B, stroke_width=3))
        own = VGroup(tx("Own it", 22, OWN, bold=True), tx(f"buy the lot now for ${U['lot']:.0f}k", 16, WHITE),
                     tx(f"and carry it: money costs {100 * U['carry']:.0f}% a year", 16, GREY_A)).arrange(DOWN, buff=0.12).move_to([-3.4, -1.2, 0])
        opt = VGroup(tx("Option it", 22, OPTION, bold=True), tx(f"put down ${U['deposit']:.0f}k now; buy the lot at delivery", 16, WHITE),
                     tx(f"at a price that grows {100 * U['escalator']:.0f}% a year, or walk away", 16, GREY_A)).arrange(DOWN, buff=0.12).move_to([3.4, -1.2, 0])
        est = estimate_tag("the Works: an illustrative builder and lot", size=12)
        beat(self,
             f"Here is the deal. <bookmark mark='a'/> A finished lot costs {U['lot']:.0f} thousand dollars today; a home "
             f"built on it sells for {U['price']:.0f} thousand at today's prices. <bookmark mark='b'/> You can own the lot: "
             f"buy it now, and carry the cost of the money tied up in it, {100 * U['carry']:.0f} per cent a year. "
             f"<bookmark mark='c'/> Or you can option it: put down a {U['deposit']:.0f} thousand dollar deposit now, and buy "
             f"the lot when you need it at a price that rises {100 * U['escalator']:.0f} per cent a year, the return the "
             "landowner or a land banker wants for holding it for you. If the market turns, you walk away and lose only "
             "the deposit.",
             base=[est], steps=[[lot, arrows, frame, house], own, opt])

    def dollar(self):
        U = R["run"]
        P = U["price"]
        parts = [("the lot", U["lot"] / P, LAND), ("the house: materials and trades", U["build"] / P, HOUSE),
                 ("selling and overhead", U["overhead"], ALL), ("profit", U["margin_now"], PRICE)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}c", 22, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        est = estimate_tag("the Works' home at today's price", size=12)
        beat(self,
             f"At today's prices, a dollar of the home's {P:.0f} thousand dollar price splits like this. "
             f"<bookmark mark='a'/> {100 * U['lot'] / P:.0f} cents for the lot, <bookmark mark='b'/> "
             f"{100 * U['build'] / P:.0f} cents for the house itself, the materials and the trades, <bookmark mark='c'/> "
             f"{100 * U['overhead']:.0f} for selling it and running the company, <bookmark mark='d'/> and "
             f"{100 * U['margin_now']:.0f} cents of profit. But you will not sell it at today's price; you will sell it in "
             f"{U['years']} years.",
             base=[est], steps=[[bar[i], labs[i]] for i in range(4)])

    def states(self):
        U = R["run"]
        items = [("today", U["price"], ALL, f"${U['price']:.0f}k"),
                 (f"in {U['years']} years, if rates fall or hold", U["sale"]["boom"], GOOD, f"${U['sale']['boom']:.0f}k"),
                 (f"in {U['years']} years, if rates rise", U["sale"]["bust"], BAD, f"${U['sale']['bust']:.0f}k")]
        rows = hbars(items, max_value=480, x0=0.4, top=1.2, row=1.0, length=5.6, size=17, bar_h=0.5)
        lab = tx("the home's price", 16, GREY_A).move_to([0, 2.2, 0])
        est = estimate_tag(f"the Works: a bust has a {100 * U['p_bust']:.0f}% chance", size=12)
        beat(self,
             "Two futures. <bookmark mark='a'/> The home sells today for "
             f"{U['price']:.0f} thousand. <bookmark mark='b'/> If mortgage rates fall or hold, in {U['years']} years it sells "
             f"for {U['sale']['boom']:.0f} thousand. <bookmark mark='c'/> If rates rise and buyers can afford less, for "
             f"{U['sale']['bust']:.0f} thousand. Say the bad case has a {100 * U['p_bust']:.0f} per cent chance: houses "
             "have had both kinds of three years in the last twenty.",
             base=[rows.axis, lab, est], steps=[rows[0], rows[1], rows[2]])

    def compare(self):
        T = R["run"]["table"]
        rows = [["", "prices up", "prices down", "on average"]]
        for k, nm, c in (("own", "own the lot", OWN), ("option", "option the lot", OPTION)):
            rows.append([nm] + [("-" if T[k][s] < 0 else "+") + f"${abs(T[k][s]):.1f}k" for s in ("boom", "bust", "expected")])
        tbl = table(rows, col_x=[-5.4, -1.8, 0.9, 3.6], top=1.2, row_h=0.9, size=21,
                    colors=[None, [OWN, GOOD, BAD, OWN], [OPTION, GOOD, BAD, OPTION]])
        lab = tx("profit per home", 16, GREY_A).move_to([0, 2.2, 0])
        est = estimate_tag("the Works' builder", size=12)
        beat(self,
             "Now the profit on each home. <bookmark mark='a'/> If you own the lot: when prices rise you make "
             f"{T['own']['boom']:.0f} thousand dollars a home, but when they fall you lose {abs(T['own']['bust']):.0f} "
             f"thousand, because you paid for the land, and carried it, at yesterday's price. On average, "
             f"{T['own']['expected']:.0f} thousand. <bookmark mark='b'/> If you option it: when prices rise you make "
             f"{T['option']['boom']:.0f} thousand, less, because the land banker took its return; when they fall you walk "
             f"away and lose the {abs(T['option']['bust']):.0f} thousand deposit. On average, {T['option']['expected']:.0f} "
             "thousand: a little less, with a much smaller worst case.",
             base=[tbl[0], lab, est], steps=[tbl[1], tbl[2]])

    def capital(self):
        T = R["run"]["table"]
        c = stat_cards([(f"${T['own']['capital']:.0f}k", "tied up per home if you own the lot", OWN),
                        (f"${T['option']['capital']:.0f}k", "tied up per home if you option it", OPTION)], y=1.2, size=44, span=10)
        r = stat_cards([(f"{100 * T['own']['return']:.0f}%", "average profit per dollar tied up, owning", OWN),
                        (f"{100 * T['option']['return']:.0f}%", "the same, optioning", OPTION)], y=-1.2, size=44, span=10)
        est = estimate_tag("the Works' builder, over three years", size=12)
        beat(self,
             "And the money it takes. <bookmark mark='a'/> Owning ties up the whole "
             f"{T['own']['capital']:.0f} thousand dollar lot for three years; optioning ties up the "
             f"{T['option']['capital']:.0f} thousand deposit. <bookmark mark='b'/> So per dollar a builder has, the option "
             f"earns far more: on average {100 * T['option']['return']:.0f} per cent over the three years against "
             f"{100 * T['own']['return']:.0f} per cent. A builder that options its land can build many more homes with the "
             "same money, and survive a bad year.",
             base=[est], steps=[c, r])

    def sweep(self):
        U = R["run"]
        own = {100 * p: v[0] for p, v in U["sweep"].items()}
        opt = {100 * p: v[1] for p, v in U["sweep"].items()}
        ch = line_chart({"own": (own, OWN), "option": (opt, OPTION)}, x=(0, 100), y=(-30, 60), xticks=[0, 20, 40, 60, 80, 100],
                        yticks=[-30, -15, 0, 15, 30, 45, 60], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: ("-" if v < 0 else "") + f"${abs(v):.0f}k",
                        ylabel="average profit per home", width=9.0, height=4.2, center=(-0.6, -0.5))
        zero = DashedLine(ch.ax.c2p(0, 0), ch.ax.c2p(100, 0), stroke_color=GREY_B, stroke_width=1.5)
        b = 100 * U["breakeven"]
        m = marker(ch.ax, b, (1 - U["breakeven"]) * R["run"]["table"]["own"]["boom"] + U["breakeven"] * R["run"]["table"]["own"]["bust"],
                   f"they cross at {b:.0f}%", PRICE, side=UP)
        xl = tx("the chance that prices fall", 14, GREY_B).next_to(ch.ax, DOWN, buff=0.45)
        est = estimate_tag("the Works' builder", size=12)
        beat(self,
             "Which is better depends on how likely a fall is. <bookmark mark='a'/> If prices never fall, owning wins. "
             "If they always fall, optioning loses far less. <bookmark mark='b'/> The lines cross at about "
             f"{b:.0f} per cent: above that chance of a bust, the option earns more even per home. A builder that cannot "
             "tell which side of the line it is on, which is most of them most of the time, has a reason to option. The "
             "next two chapters show what the largest American builders do.",
             base=[ch.frame, zero, xl, est], steps=[[ch.lines["own"], ch.labels["own"], ch.lines["option"], ch.labels["option"]], m])
