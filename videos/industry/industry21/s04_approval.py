from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Approval(VoiceoverScene):
    def construct(self):
        card(self, 3, "Two roads to market", "How does a new device reach a hospital?",
             "Chapter three. Two roads to market. A new drug must prove itself in years of trials. Most new devices do not. "
             "Why?", lit=("make", "moat"))
        self.roads()
        self.counts()
        self.panels()
        self.recalls()

    def roads(self):
        k = VGroup(tx("510(k): clearance", 22, DEVICE, bold=True),
                   tx("show the device is substantially equivalent", 16, WHITE),
                   tx("to one already legally sold", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.4, 1.2, 0])
        p = VGroup(tx("Premarket approval (PMA)", 22, BAD, bold=True),
                   tx("show it is safe and effective,", 16, WHITE),
                   tx("usually with clinical studies", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, 1.2, 0])
        d = VGroup(tx("De Novo", 22, PRICE, bold=True),
                   tx("a new kind of device of low or moderate risk, with nothing to compare it to", 16, WHITE)
                   ).arrange(DOWN, buff=0.08).move_to([0, -1.2, 0])
        rk = VGroup(tx("lower risk", 15, GREY_A), Arrow(LEFT * 2.5, RIGHT * 2.5, buff=0, stroke_width=3, color=GREY_B),
                    tx("higher risk", 15, GREY_A)).arrange(RIGHT, buff=0.2).move_to([0, -2.6, 0])
        src = source("US Food and Drug Administration: premarket notification 510(k), premarket approval and De Novo "
                     "classification", size=12)
        beat(self,
             "In America a device reaches the market by one of two main roads. <bookmark mark='a'/> Most use the 510(k): "
             "the maker shows the FDA that its device is substantially equivalent to one already legally on the market, "
             "and the device is cleared. <bookmark mark='b'/> Devices of the highest risk, such as many heart valves and "
             "implanted defibrillators, need premarket approval, which usually requires clinical studies showing they are "
             "safe and effective. <bookmark mark='c'/> And a new kind of device of low or moderate risk, with nothing to "
             "compare it to, can take a third road, the De Novo request. <bookmark mark='d'/> The higher the risk, the "
             "harder the road.",
             base=[src], steps=[k, p, d, rk])

    def counts(self):
        F = R["fda"]
        sq = 0.13

        def grid(n, cols, color, x, y):
            return VGroup(*[Square(sq * 0.85, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
                [x + sq * (i % cols), y - sq * (i // cols), 0]) for i in range(n)])
        g1 = grid(round(F["k510_5"] / 10), 30, DEVICE, -6.0, 2.0)
        g2 = grid(max(1, round(F["denovo_5"] / 10)), 30, PRICE, 0.8, 2.0)
        g3 = grid(max(1, round(F["pma_5"] / 10)), 30, BAD, 3.6, 2.0)
        l1 = tx(f"510(k) clearances: {F['k510_5']:,.0f} a year", 17, DEVICE, bold=True).next_to(g1, DOWN, buff=0.25)
        l2 = tx(f"De Novo: {F['denovo_5']:.0f}", 17, PRICE, bold=True).next_to(g2, DOWN, buff=0.25)
        l3 = tx(f"new PMAs: {F['pma_5']:.0f}", 17, BAD, bold=True).next_to(g3, DOWN, buff=0.25)
        key = tx("each square: ten decisions, average of 2021-2025", 15, GREY_A).to_edge(DOWN, buff=0.9)
        src = source("US Food and Drug Administration via openFDA: 510(k), De Novo and original PMA decisions by year", size=12)
        beat(self,
             f"Count them. <bookmark mark='a'/> From 2021 to 2025 the FDA cleared about {F['k510_5']:,.0f} devices a year "
             "through the 510(k). <bookmark mark='b'/> It granted about "
             f"{F['denovo_5']:.0f} De Novo requests a year, <bookmark mark='c'/> and approved about {F['pma_5']:.0f} "
             "entirely new high-risk devices. For every device that had to prove itself from scratch, about a hundred "
             "came to market by comparison with something already there. That is one reason devices change by small steps: "
             "each new model is cleared against the last. Every one of these decisions since 1976 is public, in the FDA's "
             "own records.",
             base=[key, src], steps=[[g1, l1], [g2, l2], [g3, l3]])

    def panels(self):
        F = R["fda"]
        top = sorted(F["panels"].items(), key=lambda kv: -kv[1])[:8]
        items = [(k, v, DEVICE, f"{v}") for k, v in top]
        rows = hbars(items, x0=-0.6, top=2.2, row=0.58, length=6.0, size=16, bar_h=0.36)
        src = source("US Food and Drug Administration via openFDA: 510(k) clearances in 2025 by review panel", size=12)
        beat(self,
             "Where do they come from? Here are the 510(k) clearances of 2025 by the FDA panel that reviewed them. "
             f"<bookmark mark='a'/> Radiology led, with {top[0][1]}: scanners and the software that reads their images. "
             f"<bookmark mark='b'/> Then orthopedics, {top[1][1]}: screws, plates, joints. <bookmark mark='c'/> General and "
             f"plastic surgery, {top[2][1]}, and the heart, {top[3][1]}. <bookmark mark='d'/> Down to dental, "
             "neurology and the hospital's general supplies.",
             base=[rows.axis, head("510(k) clearances in 2025, by review panel"), src],
             steps=[rows[0], rows[1], VGroup(rows[2], rows[3]), VGroup(*rows[4:])])

    def recalls(self):
        F = R["fda"]
        rc = F["recall_c1"]
        items = [(str(y)[2:], v, BAD, f"{v}") for y, v in sorted(rc.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.6, width=0.55, gap=0.22, size=12)
        note = tx("Class I: a reasonable probability of serious harm or death", 16, BAD, bold=True).to_edge(UP, buff=0.9)
        src = source("US Food and Drug Administration via openFDA: device recall enforcement reports, Class I, by report date",
                     size=12)
        hi = max(rc, key=rc.get)
        beat(self,
             "The other end of the road is the recall. <bookmark mark='a'/> The FDA classes the most serious recalls as "
             "Class I: a reasonable probability that using the product will cause serious harm or death. "
             "<bookmark mark='b'/> Counted by the products named in its reports, Class I recalls have swung between "
             f"about {min(rc.values())} and {rc[hi]} a year since 2012. <bookmark mark='c'/> One recall can name many "
             f"products: in 2023 the {rc[2023]} came from {F['c1_events']} recall events, the largest naming {F['c1_max']}. "
             "A device cleared by comparison is watched after it is sold.",
             base=[head("Products in Class I device recalls, by year"), src], steps=[note, VGroup(*bars_[:7]), VGroup(*bars_[7:])])
