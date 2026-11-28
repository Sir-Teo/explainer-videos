from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Turns(VoiceoverScene):
    def construct(self):
        card(self, 3, "Turns and the float", "How do you earn a good return on two cents a dollar?",
             "Chapter three. Turns and the float. A thin margin on goods that sell fast, paid for with the suppliers' "
             "money, can earn a very good return.", lit=("dollar", "moat"))
        self.days()
        self.shelves()
        self.float_()
        self.turns()

    def days(self):
        F = R["turns"]["float"]
        w = F["Walmart"]
        line = NumberLine(x_range=[0, 50, 10], length=11, include_numbers=True, font_size=22).move_to([0, -0.4, 0])
        inv = Line(line.n2p(0), line.n2p(w["inv_days"]), stroke_color=GOODS, stroke_width=14).shift(UP * 0.6)
        il = tx(f"goods sit on the shelf: {w['inv_days']:.0f} days", 17, GOODS, bold=True).next_to(inv, UP, buff=0.12)
        pay = Line(line.n2p(0), line.n2p(w["pay_days"]), stroke_color=GOOD, stroke_width=14).shift(DOWN * 0.6 + DOWN * 0.4)
        pl = tx(f"Walmart pays the supplier after: {w['pay_days']:.0f} days", 17, GOOD, bold=True).next_to(pay, DOWN, buff=0.12)
        lab = tx("Walmart, year to January 2026: inventory and accounts payable in days of cost of goods", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Walmart, Form 10-K for fiscal 2026, via SEC company facts (this series' arithmetic)", size=12)
        beat(self,
             "Here is the trick that makes thin margins work. <bookmark mark='a'/> A tin of beans reaches a Walmart shelf "
             f"and sits there, on average, about {w['inv_days']:.0f} days before it is sold. <bookmark mark='b'/> But "
             f"Walmart pays the supplier who made it, on average, after about {w['pay_days']:.0f} days. It has sold the beans "
             "before it pays for them.",
             base=[line, lab, src], steps=[VGroup(inv, il), VGroup(pay, pl)])

    def shelves(self):
        F = R["turns"]["float"]
        order = ["Costco", "Albertsons", "Amazon", "Walmart", "Target", "Dollar General"]
        items = [(k, F[k]["inv_days"], CLUB if k == "Costco" else (DOLLAR if k == "Dollar General" else MASS), f"{F[k]['inv_days']:.0f} days") for k in order]
        rows = hbars(items, max_value=85, x0=0.4, top=1.9, row=0.72, length=5.6, size=17, bar_h=0.4)
        lab = tx("how long goods sit before they are sold: inventory in days of cost of goods, latest year", 16, GREY_A).to_edge(UP, buff=0.7)
        src = source("Forms 10-K via SEC company facts (this series' arithmetic)", size=12)
        beat(self,
             f"How fast do the goods move elsewhere? <bookmark mark='a'/> At Costco goods sit about {F['Costco']['inv_days']:.0f} days; at Albertsons, a supermarket full of "
             f"fresh food, {F['Albertsons']['inv_days']:.0f}. <bookmark mark='b'/> Walmart and Target, with clothes, toys "
             f"and electronics as well as food, {F['Walmart']['inv_days']:.0f} and {F['Target']['inv_days']:.0f}; Dollar "
             f"General, {F['Dollar General']['inv_days']:.0f}. The faster the shelf empties, the less money the shop has "
             "tied up in it.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:3]), VGroup(*rows[3:])])

    def float_(self):
        F = R["turns"]["float"]
        order = ["Amazon", "Walmart", "Costco", "Target", "Albertsons", "Dollar General"]
        items = [(k, F[k]["funded"], GOOD if F[k]["funded"] > 0 else BAD, f"{'+' if F[k]['funded'] > 0 else '-'}${abs(F[k]['funded']):.1f}bn") for k in order]
        rows = hbars([(n, abs(v), c, t) for n, v, c, t in items], max_value=90, x0=0.4, top=1.9, row=0.72, length=5.6, size=17, bar_h=0.4)
        lab = tx("money owed to suppliers less money tied up in goods, latest year-end", 17, GREY_A).to_edge(UP, buff=0.7)
        src = source("Forms 10-K via SEC company facts (accounts payable less inventory)", size=12)
        beat(self,
             "Add it up across the company. <bookmark mark='a'/> At its last year-end Walmart owed its suppliers about "
             f"{F['Walmart']['funded']:.1f} billion dollars more than it had tied up in goods; Costco, "
             f"{F['Costco']['funded']:.1f} billion. Amazon, which pays its suppliers about "
             f"{F['Amazon']['pay_days']:.0f} days after buying, {F['Amazon']['funded']:.0f} billion. <bookmark mark='b'/> "
             f"Dollar General is the other way round: its goods sit {F['Dollar General']['inv_days']:.0f} days, and it "
             "carries them with its own money. The suppliers are, in effect, lending the biggest retailers their stock for "
             "free.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:4]), VGroup(*rows[4:])])

    def turns(self):
        Ro = R["turns"]["roa"]
        rows = [["", "keeps per dollar", "x", "sales per $ of assets", "=", "return on assets"]]
        for k in ("Costco", "Walmart", "Target", "Dollar General", "Kroger"):
            v = Ro[k]
            rows.append([k, f"{v['margin']:.1f}c", "x", f"{v['turns']:.2f}", "=", f"{v['margin'] * v['turns']:.1f}%"])
        t = table(rows, col_x=[-6.2, -3.4, -1.6, -0.9, 3.4, 4.1], top=1.9, row_h=0.62, size=17,
                  colors=[None] + [[CLUB, WHITE, GREY_B, WHITE, GREY_B, GOOD]] + [[MASS, WHITE, GREY_B, WHITE, GREY_B, GOOD]] * 3 + [[GROCER, WHITE, GREY_B, WHITE, GREY_B, BAD]])
        src = source("Forms 10-K via SEC company facts, latest fiscal year (net income; revenue over total assets)", size=12)
        c, k = Ro["Costco"], Ro["Kroger"]
        beat(self,
             "And the speed matters as much as the margin. <bookmark mark='a'/> Costco keeps "
             f"{c['margin']:.1f} cents of each dollar, but every dollar of its assets turns over {c['turns']:.1f} dollars of "
             f"sales a year, so it earns about {c['margin'] * c['turns']:.0f} per cent a year on what it owns. "
             "<bookmark mark='b'/> Walmart, Target and Dollar General keep a little more and turn a little slower. "
             f"<bookmark mark='c'/> Kroger turns fast too, but kept only {k['margin']:.1f} cents in its last year, after "
             "writing off its automated warehouses: about two per cent a year. Margin times turns is the whole game.",
             base=[src, t[0]], steps=[t[1], VGroup(t[2], t[3], t[4]), t[5]])
