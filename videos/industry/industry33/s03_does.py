from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Does(VoiceoverScene):
    def construct(self):
        card(self, 2, "What a wholesaler does", "What exactly is the customer paying the middleman for?",
             "Chapter two. What a wholesaler does. Four jobs, each of which the maker or the shop could do for itself, and "
             "usually chooses not to.", lit=("unit", "make"))
        self.jobs()
        self.links()
        self.credit()
        self.networks()

    def jobs(self):
        p = draw.pallet(1.6).move_to([-5.2, 0.9, 0])
        sh = draw.shelf(1.8, rows=3, n=4).move_to([-1.8, 0.9, 0])
        inv = draw.invoice(1.1, terms="net 30").move_to([1.6, 0.9, 0])
        vn = draw.van(1.6, color=DRUG).move_to([5.0, 0.7, 0])
        labs = VGroup(*[tx(t, 17, c, bold=True) for t, c in (("break bulk", GOODS), ("hold the stock", IND), ("give credit", BAD), ("deliver tomorrow", DRUG))])
        for l_, obj in zip(labs, (p, sh, inv, vn)):
            l_.next_to(obj, DOWN, buff=0.3)
        subs = VGroup(*[tx(t, 13, GREY_A) for t in ("a pallet becomes a box or two", "so the shop does not need a stockroom",
                                                     "the shop pays when it has sold", "small orders, many stops")])
        for s_, l_ in zip(subs, labs):
            s_.next_to(l_, DOWN, buff=0.1)
        tag = estimate_tag("this series' summary", size=12)
        beat(self,
             "<bookmark mark='a'/> First, it breaks bulk: the maker sells by the pallet, the pharmacy or the restaurant "
             "buys by the box. <bookmark mark='b'/> Second, it holds the stock, so that the shop needs no stockroom of its "
             "own and the maker need not guess what each shop will want. <bookmark mark='c'/> Third, it gives credit: "
             "thousands of small customers pay weeks later, and the wholesaler, not the maker, judges whether they will "
             "pay at all. <bookmark mark='d'/> Fourth, it delivers, every day if need be, many small orders on one route.",
             base=[tag], steps=[VGroup(p, labs[0], subs[0]), VGroup(sh, labs[1], subs[1]), VGroup(inv, labs[2], subs[2]), VGroup(vn, labs[3], subs[3])])

    def links(self):
        L = VGroup(*[draw.factory(0.55) for _ in range(5)]).arrange(DOWN, buff=0.18).move_to([-5.6, 0.3, 0])
        Rr = VGroup(*[draw.shop(0.45, color=DRUG) for _ in range(6)]).arrange(DOWN, buff=0.12).move_to([-1.4, 0.3, 0])
        direct = VGroup(*[Line(a.get_right(), b.get_left(), stroke_width=1.2, stroke_color=GREY_B) for a in L for b in Rr])
        L2 = L.copy().move_to([1.6, 0.3, 0])
        R2 = Rr.copy().move_to([5.8, 0.3, 0])
        hub = draw.warehouse(1.2, docks=3, trucks=0).move_to([3.7, 0.3, 0])
        via = VGroup(*[Line(a.get_right(), hub.get_left(), stroke_width=1.6, stroke_color=GOODS) for a in L2],
                     *[Line(hub.get_right(), b.get_left(), stroke_width=1.6, stroke_color=DRUG) for b in R2])
        t1 = tx("5 makers x 6 shops = 30 accounts", 17, GREY_A).move_to([-3.5, -2.1, 0])
        t2 = tx("5 + 6 = 11 accounts", 17, GOOD).move_to([3.7, -2.1, 0])
        big = tx("1,000 makers and 10,000 pharmacies: 10 million links, or 11,000", 19, WHITE, bold=True).to_edge(DOWN, buff=0.75)
        tag = estimate_tag("illustration", size=12)
        beat(self,
             "Why does it pay? Count the links. <bookmark mark='a'/> If five makers each sold straight to six shops, "
             "there would be thirty accounts to open, thirty deliveries to plan, thirty invoices to chase. "
             "<bookmark mark='b'/> Put one wholesaler in the middle and there are eleven. <bookmark mark='c'/> Now make it a "
             "thousand makers and ten thousand pharmacies: ten million relationships, or eleven thousand. The middleman "
             "is the cheapest way to connect many to many, which is why it survives every attempt to cut it out.",
             base=[tag], steps=[VGroup(L, Rr, direct, t1), VGroup(L2, R2, hub, via, t2), big])

    def credit(self):
        rec = R["returns"]["days"]["McKesson"]
        inv = draw.invoice(1.6, terms="net 25").move_to([-4.6, 0.4, 0])
        c = stat_cards([(f"${R['hook']['big3']['MCK']['rev'] * rec['rec'] / 365:.0f}bn", "owed to McKesson by its customers, March 2026", DRUG),
                        (f"{get('mk33.cvs.ar'):.0f}%", "of it owed by one customer, CVS Health", BAD),
                        (f"{rec['rec']:.0f} days", "the average wait to be paid", GOODS)], y=0.4, size=32, span=8.6)
        c.shift(RIGHT * 2.0)
        src = source("McKesson, Form 10-K for fiscal 2026; balance sheet via SEC company facts", size=12)
        beat(self,
             "Take the third job, credit, because it is the least visible. <bookmark mark='a'/> At the end of March 2026, "
             f"McKesson's customers owed it about {R['hook']['big3']['MCK']['rev'] * rec['rec'] / 365:.0f} billion dollars "
             f"for medicines already delivered. <bookmark mark='b'/> About {get('mk33.cvs.ar'):.0f} per cent of that was owed "
             f"by a single customer. <bookmark mark='c'/> On average a customer took {rec['rec']:.0f} days to pay. A drug "
             "maker selling to thousands of pharmacies would have to judge each one's credit for itself; the wholesaler does "
             "it once, for everyone, and carries the loss when a customer fails.",
             base=[inv, src], steps=[c[0], c[1], c[2]])

    def networks(self):
        D = R["does"]
        c = stat_cards([(f"{D['sysco']:.0f}", "Sysco's distribution facilities, June 2026", FOOD),
                        (f"{D['usf_cust'] / 1e3:.0f}k", "customer locations US Foods supplies", FOOD),
                        (f"{D['usf_trucks']:,.0f}", "US Foods' trucks", FOOD),
                        (f"{D['gww_stocked']:.1f}m", "products Grainger keeps in stock", IND),
                        (f"{D['mck_dcs']:.0f}", "McKesson's US drug distribution centers", DRUG)], y=0.4, size=32, span=12.8)
        trucks = VGroup(*[draw.semi(1.6, cab_color=FOOD) for _ in range(3)]).arrange(RIGHT, buff=0.4).move_to([0, -2.0, 0])
        src = source("Sysco, Form 10-K for fiscal 2026; US Foods, Grainger and McKesson, Forms 10-K", size=12)
        beat(self,
             f"And the real networks are vast. <bookmark mark='a'/> Sysco, which supplies restaurants, ran {D['sysco']:.0f} "
             f"distribution facilities in 2026. <bookmark mark='b'/> US Foods supplies about {D['usf_cust'] / 1e3:.0f} "
             f"thousand customer locations, <bookmark mark='c'/> with more than {D['usf_trucks']:,.0f} trucks. "
             f"<bookmark mark='d'/> Grainger, which sells to factories and maintenance crews, keeps "
             f"{D['gww_stocked']:.1f} million different products in stock. <bookmark mark='e'/> And McKesson supplies "
             f"American pharmacies from just {D['mck_dcs']:.0f} distribution centers: each one serves a whole region.",
             base=[trucks, src], steps=[c[0], c[1], c[2], c[3], c[4]])
