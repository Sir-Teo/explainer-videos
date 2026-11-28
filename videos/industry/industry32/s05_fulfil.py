from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Fulfil(VoiceoverScene):
    def construct(self):
        card(self, 4, "Getting it there", "Why is fast delivery a game for the biggest?",
             "Chapter four. Getting it there. The website is the cheap part. The expensive part is the warehouses, the "
             "people in them, and a van at your door.", lit=("make", "moat"))
        self.path()
        self.curve()
        self.shipping()
        self.jobs()
        self.others()

    def path(self):
        wh = draw.warehouse(4.2, docks=6, trucks=2).move_to([-3.8, 1.3, 0])
        bots = VGroup(*[draw.drive_robot(0.7, pod=True) for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to([2.6, 1.4, 0])
        belt = draw.conveyor(5.0, n=7, item_color=BRAND).move_to([-2.6, -1.3, 0])
        vans = VGroup(*[draw.van(1.2, color=SHOP) for _ in range(2)]).arrange(RIGHT, buff=0.4).move_to([1.8, -1.3, 0])
        homes = VGroup(*[draw.house(0.6) for _ in range(3)]).arrange(RIGHT, buff=0.25).move_to([5.3, -1.3, 0])
        l1 = tx("store: goods arrive in bulk and are shelved", 14, GREY_A).next_to(wh, DOWN, buff=0.15)
        l2 = tx("pick: by hand, or with robots that bring the shelf", 14, GREY_A).next_to(bots, DOWN, buff=0.15)
        l3 = tx("pack and sort, by postcode", 14, GREY_A).next_to(belt, DOWN, buff=0.15)
        l4 = tx("the last mile", 14, GREY_A).next_to(vans, DOWN, buff=0.15)
        beat(self,
             "Here is the path of a parcel. <bookmark mark='a'/> Goods arrive at a fulfilment centre by the lorry-load and "
             "are put away on shelves. <bookmark mark='b'/> When you order, someone takes your item off the shelf; in "
             "some warehouses robots carry the shelf to the picker, to save walking. <bookmark mark='c'/> It is packed, labelled and sorted with "
             "thousands of others by where they are going. <bookmark mark='d'/> And a van brings it the last mile, the most "
             "expensive mile, because it stops at every door.",
             base=[], steps=[VGroup(wh, l1), VGroup(bots, l2), VGroup(belt, l3), VGroup(vans, homes, l4)])

    def curve(self):
        C = R["run"]["cpo"]
        ser = {f"{d:.0f}-day promise": ({n: C[n][d] for n in C}, col) for d, col in ((1.0, BAD), (2.0, MARKET), (3.0, GOOD))}
        ch = line_chart(ser, x=(0, 8), y=(0, 26), xticks=[0, 2, 4, 6, 8], yticks=[0, 5, 10, 15, 20, 25],
                        xfmt=lambda v: f"{v:.0f}bn", yfmt=lambda v: f"${v:.0f}", ylabel="the Works: cost of delivering an order, by orders a year",
                        width=8.6, height=4.3, center=(-1.2, -0.45), nudge={"1-day promise": 0.25, "3-day promise": -0.25})
        tag = estimate_tag("the Works: a fixed network that grows with speed, shared over every order", size=12)
        beat(self,
             "Why does size matter so much? <bookmark mark='a'/> A delivery network is mostly a fixed cost: the buildings, "
             "the sorting machines, the routes. Promise delivery in three days and a modest network will do; at a quarter "
             f"of a billion orders a year an order costs about ${C[0.25][3.0]:.0f}. <bookmark mark='b'/> Promise two days and "
             f"you need twice the network, ${C[0.25][2.0]:.0f} an order at that size. <bookmark mark='c'/> Promise one day "
             f"and it is ${C[0.25][1.0]:.0f}. But follow the curves to the right: at eight billion orders, one-day delivery "
             f"costs ${C[8][1.0]:.0f}, close to what a three-day promise costs a small rival. Speed is affordable only at scale.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["3-day promise"], ch.labels["3-day promise"]),
                                          VGroup(ch.lines["2-day promise"], ch.labels["2-day promise"]),
                                          VGroup(ch.lines["1-day promise"], ch.labels["1-day promise"])])

    def shipping(self):
        F = R["fulfil"]
        ch = line_chart({"shipping costs": (F["ship"], BAD), "third-party seller services": (F["threep"], MARKET)},
                        x=(2015, 2025), y=(0, 180), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 60, 120, 180],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="Amazon, $bn a year", width=8.4, height=4.3, center=(-1.4, -0.45),
                        nudge={"shipping costs": -0.25})
        s = F["ship"]
        m = marker(ch.ax, 2020, s[2020], f"2020: ${s[2020]:.0f}bn", BAD, side=DOWN + RIGHT)
        src = source("Amazon.com, Forms 10-K for 2017-2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Amazon's shipping costs were {s[2015]:.1f} billion dollars in 2015 and "
             f"{s[2025]:.1f} billion in 2025, nine times as much. <bookmark mark='b'/> The steepest climb was in 2020, when "
             f"orders surged during the pandemic and the cost jumped to {s[2020]:.0f} billion. <bookmark mark='c'/> Over the "
             "same decade, the fees sellers paid it rose even faster, and part of that is sellers paying Amazon to store and "
             "deliver their goods: the network built for Amazon's own shop became a service it sells.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["shipping costs"], ch.labels["shipping costs"]), m,
                                         VGroup(ch.lines["third-party seller services"], ch.labels["third-party seller services"])])

    def jobs(self):
        F = R["fulfil"]
        ch = line_chart({"warehousing and storage": (F["ware"], BRAND), "couriers and messengers": (F["courier"], SHOP)},
                        x=(2000, 2027), y=(0, 2000), xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 500, 1000, 1500, 2000],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1e3:.1f}m", ylabel="Americans employed (seasonally adjusted)",
                        width=8.6, height=4.3, center=(-1.2, -0.45))
        w, c = F["ware"], F["courier"]
        w0, wl, wp = w[min(w)], w[max(w)], max(w.values())
        src = source("BLS, all employees in warehousing and storage and in couriers and messengers, via FRED", size=12)
        beat(self,
             "The network is people too. <bookmark mark='a'/> American warehouses employed about "
             f"{w0 / 1e3:.1f} million people in 2000, reached {wp / 1e3:.2f} million in 2022, and employ "
             f"{wl / 1e3:.2f} million now. <bookmark mark='b'/> Couriers and messengers, the people in the vans, rose from "
             f"{c[min(c)] / 1e3:.2f} million to {c[max(c)] / 1e3:.2f} million. Amazon alone had about "
             f"{F['emp'] / 1e6:.2f} million employees worldwide at the end of 2025.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["warehousing and storage"], ch.labels["warehousing and storage"]),
                                         VGroup(ch.lines["couriers and messengers"], ch.labels["couriers and messengers"])])

    def others(self):
        F = R["fulfil"]
        c = stat_cards([(f"{F['coupang_sqft']:.0f}m sq ft", "Coupang's warehouses and depots, Korea and Taiwan", SHOP),
                        (f"RMB{F['jd_fulfil']:.0f}bn", "JD.com's fulfilment expense, 2025", SHOP),
                        (f"{get('cp32.cust'):.1f}m", "Coupang's active customers, end of 2025", SHOP)], y=0.6, size=34, span=12.4)
        bots = VGroup(*[draw.drive_robot(0.55) for _ in range(5)]).arrange(RIGHT, buff=0.4).move_to([0, -1.9, 0])
        src = source("Coupang, Form 10-K for 2025; JD.com, Form 20-F for 2025", size=12)
        beat(self,
             "The pattern repeats wherever online shopping has won. <bookmark mark='a'/> In South Korea, Coupang built over "
             f"{F['coupang_sqft']:.0f} million square feet of warehouses and depots and promises next-day and even dawn "
             f"delivery. <bookmark mark='b'/> In China, JD.com spent {F['jd_fulfil']:.0f} billion yuan on fulfilment in "
             f"2025. <bookmark mark='c'/> Coupang's reward is {get('cp32.cust'):.1f} million customers who ordered in the last "
             "quarter of 2025. In this series' reading, the companies that own the network own the customer's "
             "expectation of speed, and rivals must match it or explain why they cannot.",
             base=[bots, src], steps=[c[0], c[1], c[2]])
