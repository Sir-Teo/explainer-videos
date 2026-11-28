from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Home(VoiceoverScene):
    def construct(self):
        card(self, 7, "The wire to the home", "Who brings the internet into the house, and who is losing?",
             "Chapter seven. The wire to the home. The cable companies are losing home internet customers, and fibre and "
             "the phone networks are winning them.", lit=("change", "moat"))
        self.flows()
        self.stocks()
        self.cable_mobile()
        self.deals()

    def flows(self):
        H = R["home"]
        items = [(n, abs(v), BAD if v < 0 else GOOD, f"{'+' if v > 0 else '-'}{abs(v):,}k") for n, v in H["changes"][:4]]
        rows = hbars(items, max_value=1000, x0=0.8, top=1.7, row=0.9, length=5.0, size=17, bar_h=0.45)
        lab = tx("home broadband customers gained or lost in 2025, thousands", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 of Comcast, Charter, Verizon and AT&T", size=12)
        beat(self,
             "Here is 2025 in four numbers. <bookmark mark='a'/> Comcast, the largest cable company, lost 711 thousand "
             f"broadband customers, ending the year with {H['comcast'] / 1e3:.1f} million. <bookmark mark='b'/> Charter lost "
             f"about {abs(H['changes'][1][1])} thousand. <bookmark mark='c'/> Verizon added {H['changes'][2][1]} thousand "
             "homes on fixed wireless, internet delivered over its mobile network to a box by the window, "
             f"<bookmark mark='d'/> and AT&T added {H['changes'][3][1]} thousand of its own, on top of "
             f"{H['att_fiber']:.1f} million fibre connections.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def stocks(self):
        H = R["home"]
        items = [("Comcast broadband", H["comcast"] / 1e3, CABLE, f"{H['comcast'] / 1e3:.1f}m"),
                 ("Charter internet", H["charter"] / 1e3, CABLE, f"{H['charter'] / 1e3:.1f}m"),
                 ("AT&T fibre", H["att_fiber"], "#4F8FE6", f"{H['att_fiber']:.1f}m"),
                 ("Verizon Fios internet (consumer)", H["vz_fios"] / 1e3, WIRELESS, f"{H['vz_fios'] / 1e3:.1f}m"),
                 ("Verizon fixed wireless (consumer)", H["vz_fwa"] / 1e3, WIRELESS, f"{H['vz_fwa'] / 1e3:.1f}m"),
                 ("AT&T Internet Air", H["att_aia"], "#4F8FE6", f"{H['att_aia']:.1f}m")]
        rows = hbars(items, max_value=34, x0=0.8, top=2.0, row=0.68, length=5.0, size=16, bar_h=0.36)
        lab = tx("home internet customers, end of 2025", 17, GREY_A).to_edge(UP, buff=0.6)
        src = source("Forms 10-K for 2025 of Comcast, Charter, AT&T and Verizon", size=12)
        beat(self,
             "The stocks still favour cable. <bookmark mark='a'/> Comcast and Charter together had about "
             f"{(H['comcast'] + H['charter']) / 1e3:.0f} million home internet customers at the end of 2025. "
             f"<bookmark mark='b'/> AT&T had {H['att_fiber']:.1f} million on fibre and Verizon {H['vz_fios'] / 1e3:.1f} million "
             f"on its Fios network. <bookmark mark='c'/> The newest, fixed wireless, had {H['vz_fwa'] / 1e3:.1f} million at "
             f"Verizon and {H['att_aia']:.1f} million at AT&T. The flows run one way, and the stocks follow slowly.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:4]), VGroup(*rows[4:])])

    def cable_mobile(self):
        H = R["home"]
        houses = VGroup(*[draw.house(0.9) for _ in range(5)]).arrange(RIGHT, buff=0.5).move_to([0, 1.8, 0])
        c = stat_cards([(f"{H['charter_mobile'] / 1e3:.1f}m", "Charter's mobile lines, end of 2025", CABLE),
                        (f"+{H['changes'][4][1] / 1e3:.1f}m", "added in 2025", GOOD),
                        ("Verizon's", "network they run on", WIRELESS)], y=-0.6, size=36, span=12)
        src = source("Charter Communications, Form 10-K for 2025", size=12)
        beat(self,
             "The cable companies' answer is to sell phones. <bookmark mark='a'/> Charter had "
             f"{H['charter_mobile'] / 1e6 * 1e3:.1f} million mobile lines at the end of 2025, <bookmark mark='b'/> "
             f"{H['changes'][4][1] / 1e3:.1f} million more than a year before, <bookmark mark='c'/> carried on Verizon's "
             "network, which it rents. The phone companies sell home internet over their mobile networks; the cable "
             "companies sell mobile phones over a phone company's network. Everyone now sells everything, bundled, to cut "
             f"churn. Charter's average home customer paid {get('ch30.arpu'):.2f} dollars a month in 2025, against "
             f"118.71 a year before: almost no price rise at all.",
             base=[houses, src], steps=[c[0], c[1], c[2]])

    def deals(self):
        g = VGroup(tx("Buying the wire, 2025-2026", 22, WHITE, bold=True),
                   tx("Verizon completed its purchase of Frontier, a fibre company, on 20 January 2026", 18, WIRELESS),
                   tx("AT&T agreed to buy substantially all of Lumen's mass-market fibre business", 18, "#4F8FE6"),
                   tx("Charter completed its combination with Cox Communications on 19 August 2026", 18, CABLE),
                   tx("T-Mobile bought UScellular's wireless business on 1 August 2025", 18, "#F2A7B5")
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        src = source("Verizon and T-Mobile, Forms 10-K for 2025; AT&T, Forms 10-K for 2025 and 10-Q for 2026 Q3; Charter, Form 10-Q for 2026 Q3", size=12)
        beat(self,
             "And they are buying each other's wires. <bookmark mark='a'/> Verizon bought Frontier, a fibre company, "
             "completing the deal in January 2026. <bookmark mark='b'/> AT&T agreed to buy substantially all of Lumen's "
             "mass-market fibre business. <bookmark mark='c'/> Charter combined with Cox in August 2026. <bookmark mark='d'/> And "
             "T-Mobile bought UScellular's wireless business. Fewer, bigger companies, each with a mobile network and a "
             "wire to the home.",
             base=[src], steps=[g[:2], g[2], g[3], g[4]])
