from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Online(VoiceoverScene):
    def construct(self):
        card(self, 8, "Groceries online", "Who pays for picking the order and driving it to the door?",
             "Chapter eight. Groceries online. Shoppers do their own picking and their own delivery for free. Online, the "
             "grocer has to pay for both.", lit=("change", "make"))
        self.work()
        self.jump()
        self.kroger()
        self.amazon()

    def work(self):
        g = VGroup(tx("Who does the work", 21, WHITE, bold=True),
                   tx("in the store: the shopper walks the aisles, picks, queues, carries and drives home, unpaid", 18, GROCER),
                   tx("online: the grocer pays someone to pick, pack and keep it cold", 18, BAD),
                   tx("and pays again, or charges, for the van to the door: Part 29's last mile", 18, BAD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.6, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        cart = draw.cart(1.4).move_to([-3.0, -2.2, 0])
        van = draw.van(1.8, color=ONLINE).move_to([3.0, -2.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Think about who does the work. <bookmark mark='a'/> In a store, the shopper walks the aisles, picks every "
             "item, queues, carries and drives home, all unpaid. <bookmark mark='b'/> Online, the grocer pays someone to "
             "pick and pack the order and keep it cold, <bookmark mark='c'/> and pays again for the van to the door, the "
             "costly last mile of Part 29. On a two-cent margin, someone has to pay for all that work: the shopper, in fees "
             "and higher prices, or the grocer, in profit. In this series' reading, that is why online grocery grew slowly "
             "for twenty years: the work the shopper did for free has a price as soon as someone else does it.",
             base=[tag], steps=[VGroup(g[:2], cart), g[2], VGroup(g[3], van)])

    def jump(self):
        E = R["traffic"]["ecom"]
        pts = [(2019.75, "end of 2019"), (2020.25, "spring 2020"), (2021.75, "end of 2021"), (max(E), "2026")]
        items = [(n, E[k], ONLINE if n != "spring 2020" else BAD, f"{E[k]:.1f}%") for k, n in pts]
        cols = vbars(items, base_y=-2.0, height=3.6, width=1.4, gap=0.7, size=16, max_value=20)
        lab = tx("online sales as a share of all American retail sales (quarterly, seasonally adjusted)", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Census Bureau, e-commerce retail sales as a percent of total, via FRED", size=12)
        beat(self,
             "The pandemic showed both sides of it. <bookmark mark='a'/> At the end of 2019, about "
             f"{E[2019.75]:.0f} per cent of American retail spending was online. <bookmark mark='b'/> In the spring of "
             f"2020, with shops shut and people afraid to go in, {E[2020.25]:.0f} per cent. <bookmark mark='c'/> Then it fell "
             f"back to about {E[2021.75]:.0f} per cent as the shops reopened, <bookmark mark='d'/> and has crept up since to "
             f"{E[max(E)]:.0f}. Shoppers proved they would buy online when they had to; most went back to the shops when "
             "they could.",
             base=[lab, src], steps=[cols[0], cols[1], cols[2], cols[3]])

    def kroger(self):
        O = R["online"]
        q1 = quote(["'The future success of the digital business will also depend on ... fulfilling orders across our",
                    "modalities, whether in store, in pickup-only locations, and through customer fulfillment centers powered by Ocado'"],
                   "Kroger, Form 10-K for fiscal 2020", size=17).move_to([0, 1.9, 0])
        wh = VGroup(*[draw.warehouse(1.6) for _ in range(3)]).arrange(RIGHT, buff=0.6).move_to([0, -0.1, 0])
        xs = VGroup(*[Cross(w, stroke_color=BAD, stroke_width=5) for w in wh])
        lab = tx(f"January 2026: three automated warehouses closed, a fourth cancelled; ${O['ocado']:.1f}bn of charges", 18, BAD, bold=True).move_to([0, -2.0, 0])
        src = source("Kroger, Forms 10-K for fiscal 2020 and fiscal 2025", size=12)
        beat(self,
             "Kroger made a bold bet on solving it with machines. <bookmark mark='a'/> It partnered with the British firm "
             "Ocado to build automated warehouses, and told investors in 2021 that its digital future depended in part on "
             "these 'customer fulfillment centers powered by Ocado'. <bookmark mark='b'/> In "
             "January 2026 it closed three of them, in Wisconsin, Maryland and Florida, which 'had not met operational or "
             "financial expectations', and cancelled a fourth. <bookmark mark='c'/> It booked "
             f"{O['ocado']:.1f} billion dollars of charges.",
             base=[src], steps=[q1, wh, VGroup(xs, lab)])

    def amazon(self):
        O = R["online"]
        ch = line_chart({"Amazon": (O["amzn"], ONLINE), "Walmart": (O["wmt"], MASS)}, x=(2015, 2025), y=(0, 800),
                        xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 200, 400, 600, 800], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="revenue, $bn a year (Walmart's years end the following January)", width=8.8, height=4.4,
                        center=(-1.2, -0.45))
        src = source("Forms 10-K via SEC company facts; Walmart, Form 10-K for fiscal 2026", size=12)
        a, w = O["amzn"], O["wmt"]
        beat(self,
             f"<bookmark mark='a'/> Walmart's revenue grew from {w[2015]:.0f} billion dollars to {w[2025]:.0f} billion over "
             f"ten years. <bookmark mark='b'/> Amazon's grew from {a[2015]:.0f} billion to {a[2025]:.0f}, and in 2025 it "
             "took in slightly more than Walmart for the first time. Walmart is growing online too, outside America as "
             f"well: its international online sales grew by {get('wm31.intl.ecom'):.1f} billion dollars in its latest year. Part 32 is about that company. For grocery, the race "
             "is still about stores: Walmart says its online growth 'was primarily driven by store-fulfilled pickup and "
             "delivery', using its thousands of stores as warehouses close to every customer.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["Walmart"], ch.labels["Walmart"]), VGroup(ch.lines["Amazon"], ch.labels["Amazon"])])
