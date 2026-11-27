from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

PROD = [("cloud", "cloud and networking: servers, network gear", "#7EC8F5"),
        ("sce", "smart consumer electronics: phones, TVs, consoles", "#F2A65A"),
        ("computing", "computing: computers, tablets", "#B58CFF"),
        ("components", "components and others: connectors, parts", "#9AA3B2")]


class HonHai(VoiceoverScene):
    def construct(self):
        card(self, 5, "Hon Hai in its own numbers", "What does the world's assembler actually make, and for whom?",
             "Chapter five. Hon Hai in its own numbers.", lit=("sold", "dollar"))
        self.products()
        self.customer()
        self.where()
        self.inside()

    def products(self):
        H = R["honhai"]
        P = H["prod"]
        sc = 5.6 / 3400
        rows = VGroup()
        for i, (k, name, col) in enumerate(PROD):
            a, b = P[k]
            y = 1.9 - 1.25 * i
            lab = tx(name, 14, WHITE, bold=True).move_to([-6.6, y + 0.5, 0], aligned_edge=LEFT)
            b24 = Rectangle(width=a * sc, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.35).move_to([-6.6, y + 0.12, 0], aligned_edge=LEFT)
            b25 = Rectangle(width=b * sc, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([-6.6, y - 0.24, 0], aligned_edge=LEFT)
            v24 = tx(f"2024: NT${a / 1000:.2f}tn", 12, GREY_A).next_to(b24, RIGHT, buff=0.1)
            v25 = tx(f"2025: NT${b / 1000:.2f}tn ({'+' if b >= a else ''}{100 * (b / a - 1):.0f}%)", 14, col, bold=True).next_to(b25, RIGHT, buff=0.1)
            rows.add(VGroup(lab, b24, v24, b25, v25))
        side = VGroup(tx("Hon Hai's revenue", 16, GREY_A), tx(f"2024: NT${H['rev24'] / 1000:.2f} trillion", 16, WHITE),
                      tx(f"2025: NT${H['rev25'] / 1000:.2f} trillion", 18, ASSEMBLER, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, 2.4, 0])
        src = source("Hon Hai, audited consolidated statements 2025, note 14 (revenue from external customers by product type)", size=13)
        with self.voiceover(
            "Hon Hai's own accounts say what it makes. <bookmark mark='a'/> In 2024 its biggest line was smart consumer "
            f"electronics, phones, televisions and game consoles: about NT${P['sce'][0] / 1000:.1f} trillion. Servers and "
            f"networking brought in NT${P['cloud'][0] / 1000:.1f} trillion. <bookmark mark='b'/> In 2025 servers and networking "
            f"jumped {100 * (P['cloud'][1] / P['cloud'][0] - 1):.0f} per cent, to NT${P['cloud'][1] / 1000:.2f} trillion, and "
            "overtook the phones, which slipped. <bookmark mark='c'/> The company best known for assembling phones now "
            "takes in more from building the machines that fill data centres."
        ) as vo:
            self.play(FadeIn(src), FadeIn(side), *[FadeIn(r_[0]) for r_ in rows], FadeIn(ghost(*[r_[3] for r_ in rows], opacity=0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[3], LEFT), FadeIn(r_[4])) for r_ in rows], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(rows[0][4], color="#7EC8F5"))
        self.clear_scene()

    def customer(self):
        H = R["honhai"]
        s24, s25 = H["client_e"]
        def donut(share, center, col):
            ring = AnnularSector(inner_radius=0.9, outer_radius=1.5, angle=TAU, start_angle=PI / 2, fill_color=GREY_D, fill_opacity=0.6, stroke_width=0)
            arc = AnnularSector(inner_radius=0.9, outer_radius=1.5, angle=-TAU * share, start_angle=PI / 2, fill_color=col, fill_opacity=0.95, stroke_width=0)
            g = VGroup(ring, arc).move_to(center)
            lab = tx(f"{100 * share:.0f}%", 34, col, bold=True).move_to(center)
            return VGroup(g, lab)
        d24 = donut(s24, [-3.2, -0.2, 0], ASSEMBLER)
        d25 = donut(s25, [2.4, -0.2, 0], ASSEMBLER)
        l24 = tx("2024", 20, WHITE, bold=True).next_to(d24, UP, buff=0.25)
        l25 = tx("2025", 20, WHITE, bold=True).next_to(d25, UP, buff=0.25)
        head = tx("Share of Hon Hai's revenue from one customer, 'Client E'", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        note = tx("The accounts do not name it.", 15, GREY_A).to_edge(DOWN, buff=0.9)
        src = source("Hon Hai, audited consolidated statements 2025, note 14 (6), major customer information", size=13)
        with self.voiceover(
            "And for whom. <bookmark mark='a'/> In 2024 a single customer, which the accounts call only 'Client E', "
            f"brought in {100 * s24:.0f} per cent of Hon Hai's revenue. <bookmark mark='b'/> In 2025, with the servers "
            f"growing, that customer's share fell to {100 * s25:.0f} per cent. Still nearly half of the biggest "
            "assembler's business, from one brand. That is the other side of the thin margin: whoever brings that much "
            "work can set the price of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(note), FadeIn(ghost(d24, d25, opacity=0.2)))
            vo.wait_until("a")
            self.play(FadeIn(l24), FadeIn(d24[0][0]), Create(d24[0][1]), FadeIn(d24[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(l25), FadeIn(d25[0][0]), Create(d25[0][1]), FadeIn(d25[1]), run_time=1.5)
        self.clear_scene()

    def inside(self):
        H = R["honhai"]
        rows = [("Foxconn Industrial Internet (servers, networking)", H["fii_rev"], H["fii_margin"], "#7EC8F5"),
                ("the rest of the Hon Hai group (phones, computers and more)", H["parent_rev"], H["parent_margin"], ASSEMBLER)]
        sc = 50.0
        bars = VGroup()
        for i, (name, rev, m, col) in enumerate(rows):
            y = 1.0 - 2.0 * i
            lab = VGroup(tx(name, 16, WHITE, bold=True), tx(f"revenue NT${rev / 1000:.1f} trillion", 13, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
                [-5.6, y + 0.6, 0], aligned_edge=LEFT)
            b = Rectangle(width=m * sc, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([-5.6, y - 0.1, 0], aligned_edge=LEFT)
            v = tx(f"operating income: {100 * m:.1f} cents per dollar", 18, col, bold=True).next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(lab, b, v))
        src = source("Hon Hai, audited consolidated statements 2025, note 14 (3): segment revenue and operating income", size=13)
        with self.voiceover(
            "Even inside Hon Hai the smile shows. <bookmark mark='a'/> Its server and networking arm, Foxconn Industrial "
            f"Internet, a separately listed company in Shanghai, made about {100 * H['fii_margin']:.1f} cents of operating "
            "income on each dollar in 2025. <bookmark mark='b'/> The rest of the group, where the phones and computers are, "
            f"made about {100 * H['parent_margin']:.1f}. In 2025, building servers paid more than three times as well, per "
            "dollar of sales, as building phones and computers."
        ) as vo:
            self.play(FadeIn(src), *[FadeIn(b_[0]) for b_ in bars], FadeIn(ghost(*[b_[1] for b_ in bars], opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
        self.clear_scene()

    def where(self):
        H = R["honhai"]
        L = H["loc"]
        tot = H["rev25"]
        names = {"us": "USA", "sg": "Singapore", "ie": "Ireland", "cn": "China", "tw": "Taiwan", "jp": "Japan", "in": "India",
                 "other": "Vietnam, Mexico, others"}
        cols = {"us": "#C9D3E0", "sg": "#7BD88F", "ie": "#B58CFF", "cn": "#E8554E", "tw": "#7EC8F5", "jp": "#E6A0C4", "in": "#F2A65A",
                "other": "#5C6472"}
        W = 12.0
        x = -W / 2
        segs, labs = VGroup(), VGroup()
        for i, k in enumerate(("us", "sg", "ie", "cn", "tw", "jp", "in", "other")):
            w = W * L[k] / tot
            r_ = Rectangle(width=w, height=1.0, stroke_color="#0E1117", stroke_width=2, fill_color=cols[k], fill_opacity=0.9).move_to([x + w / 2, 0.3, 0])
            segs.add(r_)
            lab = VGroup(tx(names[k], 14 if w > 1 else 11, WHITE, bold=True), tx(f"{100 * L[k] / tot:.0f}%", 15 if w > 1 else 12, cols[k], bold=True)).arrange(DOWN, buff=0.03)
            lab.next_to(r_, DOWN if i % 2 == 0 else UP, buff=0.12)
            labs.add(lab)
            x += w
        head = tx("Hon Hai's revenue in 2025, by where its customers are registered", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Hon Hai, audited consolidated statements 2025, note 14 (5): revenue by the customer's registered location", size=13)
        with self.voiceover(
            "Where are those customers? The accounts sort revenue by where each customer is registered. "
            f"<bookmark mark='a'/> {100 * L['us'] / tot:.0f} per cent came from customers registered in the United States, "
            f"<bookmark mark='b'/> {100 * L['sg'] / tot:.0f} per cent from Singapore and {100 * L['ie'] / tot:.0f} per cent "
            "from Ireland: not where the factories are, but where those customers' companies are registered. "
            "<bookmark mark='c'/> China, where so "
            f"many of the plants are, accounted for {100 * L['cn'] / tot:.0f} per cent. The factory is in Asia; the customer is "
            "a brand registered somewhere else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(segs, opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(segs[0], LEFT), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(segs[1], LEFT), GrowFromEdge(segs[2], LEFT), FadeIn(labs[1]), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(segs[i], LEFT), FadeIn(labs[i])) for i in range(3, 8)], lag_ratio=0.2), run_time=1.8)
        self.clear_scene()
