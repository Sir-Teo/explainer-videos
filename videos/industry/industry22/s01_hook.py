from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.products()
        self.double()
        self.spend()
        self.title()

    def products(self):
        S = R["extra"]["pg_seg_share"]
        cols = {"Fabric & Home Care": BRAND, "Baby, Feminine & Family Care": VOL, "Beauty": ADS, "Health Care": GOOD, "Grooming": PRICE}
        bar = viz.bar_split([(k, v, cols[k]) for k, v in S.items()], 100, width=12.0, height=0.9).move_to([0, 0.4, 0])
        labs = VGroup()
        ex = {"Fabric & Home Care": "Tide, Ariel, Dawn", "Baby, Feminine & Family Care": "Pampers, Always, Charmin",
              "Beauty": "Pantene, Olay", "Health Care": "Crest, Oral-B", "Grooming": "Gillette"}
        for i, (k, v) in enumerate(S.items()):
            t = VGroup(tx(f"{v}%", 20, cols[k], bold=True), tx(k, 12, GREY_A), tx(ex[k], 12, WHITE)).arrange(DOWN, buff=0.05)
            if t.width > bar[i].width + 0.2:
                t.scale_to_fit_width(bar[i].width + 0.2)
            t.next_to(bar[i], DOWN, buff=0.2)
            labs.add(t)
        src = source("The Procter & Gamble Company, Form 10-K for fiscal 2026: segments, their share of net sales and major brands", size=12)
        beat(self,
             "Open a kitchen cupboard and you may well find a few of these. <bookmark mark='a'/> Procter "
             f"and Gamble's largest business is fabric and home care, {S['Fabric & Home Care']} per cent of its sales: Tide, "
             f"Ariel, Dawn. <bookmark mark='b'/> Then nappies, feminine care and paper, {S['Baby, Feminine & Family Care']} per "
             f"cent: Pampers, Always, Charmin. <bookmark mark='c'/> Then beauty, {S['Beauty']} per cent, health care, "
             f"{S['Health Care']}, with Crest and Oral-B, <bookmark mark='d'/> and Gillette's razors, {S['Grooming']}. "
             "Everyday things, bought every week.",
             base=[src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], [bar[2], labs[2], bar[3], labs[3]], [bar[4], labs[4]]])

    def double(self):
        H = R["hook"]
        items = [("what P&G's products sold for", H["sales"], BRAND, f"${H['sales']:.1f}bn"),
                 ("what they cost to make and ship", H["cost"], STORE, f"${H['cost']:.1f}bn")]
        rows = hbars(items, max_value=95, x0=-0.4, top=0.9, row=1.2, length=6.2, size=18, bar_h=0.6)
        prods = VGroup(draw.soap(0.8), draw.detergent(1.0), draw.can(0.8, color="#7EC8F5"), draw.cereal_box(1.0)).arrange(RIGHT, buff=0.35).move_to([-3.6, 2.3, 0])
        x2 = tx(f"{H['ratio']:.2f} times", 30, PRICE, bold=True).move_to([4.6, -1.7, 0])
        src = source("The Procter & Gamble Company, Form 10-K for fiscal 2026: net sales and cost of products sold", size=12)
        beat(self,
             "Now its accounts. <bookmark mark='a'/> In the year to "
             f"June 2026 it sold {H['sales']:.1f} billion dollars of them. <bookmark mark='b'/> Making them, with the "
             f"materials, the factories and the freight, cost {H['cost']:.1f} billion. <bookmark mark='c'/> Its products "
             "sold for almost exactly twice what they cost to make. That gap, between what a product costs and what "
             "people pay for it, is what this film is about: how it is earned, and how it lasts.",
             base=[rows.axis, prods, src], steps=[rows[0], rows[1], x2])

    def spend(self):
        H = R["hook"]
        c = stat_cards([(f"${H['ads']:.1f}bn", "spent on advertising in fiscal 2026", ADS),
                        (f"{H['walmart']}%", "of its sales went to one customer, Walmart", PRICE),
                        (f"{H['top10']}%", "to its ten largest customers", WHITE)], y=0.8, size=44, span=12)
        crt = draw.cart(1.4).move_to([0, -1.7, 0])
        src = source("The Procter & Gamble Company, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Where does the other half go? <bookmark mark='a'/> A large piece goes on telling people about the products: "
             f"P&G spent {H['ads']:.1f} billion dollars on advertising that year. <bookmark mark='b'/> And the company does "
             f"not sell to you. It sells to shops: {H['walmart']} per cent of its sales went to Walmart alone, "
             f"<bookmark mark='c'/> {H['top10']} per cent to its ten largest customers. Between the brand and the shopper "
             "stands a retailer with its own shelf, and its own brand.",
             base=[crt, src], steps=[c[0], c[1], c[2]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-two: consumer goods. Why can a company charge double for soap, for a "
                            "hundred years?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
