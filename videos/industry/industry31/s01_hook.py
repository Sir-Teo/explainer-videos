from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.walmart()
        self.history()
        self.costco()
        self.title()

    def walmart(self):
        H = R["hook"]
        shops = VGroup(*[draw.shop(1.1, color=MASS) for _ in range(6)]).arrange(RIGHT, buff=0.25).move_to([0, 1.8, 0])
        c = stat_cards([(f"${H['wmt_rev']:.0f}bn", "Walmart's revenue, year to January 2026", MASS),
                        (f"{H['assoc']:.1f}m", "people working for it", ALL),
                        (f"${H['wmt_ni']:.1f}bn", "its net profit", GOOD),
                        (f"{100 * H['wmt_ni'] / H['wmt_rev']:.1f}c", "kept from each dollar", GOOD)], y=-0.6, size=34, span=12.6)
        src = source("Walmart, Form 10-K for fiscal 2026; SEC company facts", size=12)
        beat(self,
             "Walmart is the giant of selling things in shops. "
             f"<bookmark mark='a'/> In its year to January 2026 it took in {H['wmt_rev']:.0f} billion dollars. "
             f"<bookmark mark='b'/> It employs about {H['assoc']:.1f} million people. <bookmark mark='c'/> And it kept "
             f"{H['wmt_ni']:.1f} billion dollars of profit: <bookmark mark='d'/> about {100 * H['wmt_ni'] / H['wmt_rev']:.0f} "
             "cents of every dollar that passed through its tills. Almost everything a customer paid went straight back "
             "out, to the farmers and factories, the staff and the landlords. And yet three cents of seven hundred billion "
             "is a fortune, earned again every year.",
             base=[shops, src], steps=[c[0], c[1], c[2], c[3]])

    def history(self):
        Hh = R["hook"]["wmt_hist"]
        rev = {y: v[0] for y, v in Hh.items()}
        ch = line_chart({"revenue": (rev, MASS)}, x=(2010, 2025), y=(0, 800), xticks=[2010, 2013, 2016, 2019, 2022, 2025],
                        yticks=[0, 200, 400, 600, 800], yfmt=lambda v: f"${v:.0f}bn", ylabel="Walmart's revenue, $bn a fiscal year (years to January of the next)",
                        width=8.8, height=4.4, center=(-1.2, -0.45))
        ni = {y: v[1] for y, v in Hh.items()}
        nb = VGroup(*[Dot(ch.ax.c2p(y, 30 * ni[y]), radius=0.05, color=GOOD) for y in ni])
        nl = tx("net profit x 30, to be visible", 14, GOOD).next_to(nb[-1], DOWN, buff=0.2, aligned_edge=RIGHT)
        src = source("Walmart, Forms 10-K via SEC company facts", size=12)
        f, l = min(rev), max(rev)
        beat(self,
             f"<bookmark mark='a'/> Walmart's revenue has climbed from {rev[f]:.0f} billion dollars in its year to January "
             f"{f + 1} to {rev[l]:.0f} billion. <bookmark mark='b'/> Its profit has wandered between "
             f"{min(ni.values()):.0f} and {max(ni.values()):.0f} billion a year, so small beside the revenue that it has to "
             "be magnified thirty times to show on the same chart. This is the paradox of mass retail: the thinnest "
             "margins in business, and some of the biggest businesses.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["revenue"], ch.labels["revenue"]), VGroup(nb, nl)])

    def costco(self):
        H = R["hook"]
        items = [("Costco's membership fees", H["fees"], CLUB, f"${H['fees']:.1f}bn"),
                 ("Costco's net profit", H["cost_ni"], GOOD, f"${H['cost_ni']:.1f}bn")]
        rows = hbars(items, max_value=10, x0=0.4, top=1.2, row=1.2, length=5.6, size=18, bar_h=0.6)
        cart = draw.cart(1.6).move_to([-5.2, -1.8, 0])
        lab = tx("Costco, year to August 2026", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Costco Wholesale, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "And the strangest number in the industry. <bookmark mark='a'/> Costco charges its customers to shop: in its "
             f"year to August 2026 they paid {H['fees']:.1f} billion dollars in membership fees. <bookmark mark='b'/> Its "
             f"whole net profit was {H['cost_ni']:.1f} billion: the fees alone came to almost two-thirds of it. The "
             f"{H['cost_rev']:.0f} billion dollars of groceries, tyres and televisions are sold for barely more than they "
             "cost.",
             base=[rows.axis, lab, cart, src], steps=[rows[0], rows[1]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part thirty-one: grocery and mass retail. How does a business that keeps two "
                            "or three cents of every dollar become one of the largest on earth?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
