from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Delivery(VoiceoverScene):
    def construct(self):
        card(self, 7, "The app in the middle", "What does a delivery app take, and what does it keep?",
             "Chapter seven. The app in the middle. Between the restaurant and the hungry customer there is now, often, a "
             "phone app and a courier.", lit=("dollar", "change"))
        self.scale()
        self.order()
        self.split()
        self.store()

    def scale(self):
        D = R["delivery"]
        ph = draw.phone(2.0, screen=APPS).move_to([-4.6, 0.4, 0])
        c = stat_cards([(f"{D['orders'] / 1e3:.2f}bn", "orders through DoorDash in 2025", APPS),
                        (f"${D['gov']:.0f}bn", "the value of those orders", APPS),
                        (f"{D['nrm']:.1f}%", "of it kept by DoorDash as revenue", FR)], y=0.4, size=34, span=8.6)
        c.shift(RIGHT * 1.6)
        src = source("DoorDash, Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> In 2025 DoorDash carried {D['orders'] / 1e3:.1f} billion orders, <bookmark mark='b'/> worth "
             f"{D['gov']:.0f} billion dollars: meals from restaurants, groceries and other goods. "
             f"<bookmark mark='c'/> It kept {D['nrm']:.1f} per cent of that as revenue: commissions from the restaurants and "
             "fees from the customers, after paying the couriers.",
             base=[ph, src], steps=[c[0], c[1], c[2]])

    def split(self):
        D = R["delivery"]
        ni = D["ni"]
        items = [(str(y), 100 * ni[y] / D["revs"][y], GOOD if ni[y] > 0 else BAD, f"{'-' if ni[y] < 0 else ''}${abs(ni[y]):.2f}bn")
                 for y in sorted(ni) if y >= 2019]
        rows = hbars(items, max_value=80, x0=0.0, top=2.0, row=0.62, length=4.8, size=16, bar_h=0.36)
        hd = tx("DoorDash's net income: bars are its share of revenue, labels the dollars", 20, WHITE, bold=True).to_edge(UP, buff=0.5)
        src = source("DoorDash, prospectus (2020) and Forms 10-K via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> Delivery was not a profitable business for a long time. DoorDash lost {abs(ni[2019]):.2f} "
             f"billion dollars in 2019 <bookmark mark='b'/> and kept losing money for four more years, {abs(ni[2022]):.1f} billion "
             f"in 2022. <bookmark mark='c'/> It turned a profit in 2024 for the first time in the years shown, "
             f"{ni[2024] * 1e3:.0f} million, and "
             f"{ni[2025] * 1e3:.0f} million in 2025: under a cent for every dollar of orders it carried.",
             base=[rows.axis, hd, src], steps=[rows[0], VGroup(*rows[1:5]), VGroup(*rows[5:])])

    def store(self):
        U = R["run"]
        b, a30 = U["base"], U["apps30"]
        rows = [["", "share of sales through apps", "the apps' commission", "the franchisee's profit"],
                ["the Works' store today", f"{100 * U['store']['delivery']:.0f}%", k(b["apps"]), k(b["profit"])],
                ["twice as much through apps", "30%", k(a30["apps"]), k(a30["profit"])]]
        cols = [None, [WHITE, APPS, APPS, GOOD], [WHITE, APPS, APPS, BAD]]
        t = table(rows, col_x=[-6.4, -2.6, 0.8, 3.6], top=1.2, row_h=0.9, size=18, colors=cols)
        van = draw.van(1.6, color=APPS).move_to([0, -2.0, 0])
        tag = estimate_tag(f"the Works: a {100 * U['store']['commission']:.0f}% commission on delivered sales, no extra sales assumed", size=12)
        beat(self,
             "For the restaurant, an app order is a mixed blessing. <bookmark mark='a'/> In the Works, with fifteen per cent of "
             f"sales through apps at a {100 * U['store']['commission']:.0f} per cent commission, the apps take "
             f"{b['apps'] / 1e3:.0f} thousand dollars a year from a store that keeps {b['profit'] / 1e3:.0f} thousand. "
             "<bookmark mark='b'/> If those orders double without bringing new customers, the commission doubles and the "
             f"owner keeps {a30['profit'] / 1e3:.0f} thousand. A twenty per cent fee on a business with a nine per cent margin "
             "pays only if the orders are truly extra, and the fight over who keeps the customer is the real one.",
             base=[t[0], van, tag], steps=[t[1], t[2]])

    def order(self):
        D = R["delivery"]
        per = D["gov"] / D["orders"] * 1e3
        keep = per * D["nrm"] / 100
        ni = D["ni"][2025] / D["orders"] * 1e3
        c = stat_cards([(f"${per:.2f}", "an average DoorDash order, 2025", APPS),
                        (f"${keep:.2f}", "what DoorDash kept of it as revenue", FR),
                        (f"${ni:.2f}", "its net profit on it", GOOD)], y=0.5, size=40, span=11)
        bag = draw.parcel(1.0, color=APPS).move_to([0, -1.9, 0])
        src = source("DoorDash, Form 10-K for 2025; this series' division", size=12)
        beat(self,
             f"Take one order. <bookmark mark='a'/> On average a DoorDash order was worth about {per:.0f} dollars in 2025. "
             f"<bookmark mark='b'/> DoorDash kept about {keep:.2f} dollars of it as revenue, after paying the courier. "
             f"<bookmark mark='c'/> And after its engineers, its marketing and its offices, it made about {100 * ni:.0f} cents. "
             "A delivery app is a middleman of the kind Part 33 described: enormous volume, a few cents of profit on each "
             "transaction, and everything depending on density, enough orders close together to keep couriers busy.",
             base=[bag, src], steps=[c[0], c[1], c[2]])
