from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Three(VoiceoverScene):
    def construct(self):
        card(self, 6, "Three networks", "How many networks can a country carry?",
             "Chapter six. Three networks. America had four national wireless networks in 2019. Then one bought another, "
             "and the would-be fourth gave up.", lit=("moat", "change"))
        self.rise()
        self.count()
        self.alike()
        self.margins()

    def rise(self):
        T = R["three"]
        items = [(str(y), T["tm_rev"][y], WIRELESS if y < 2020 else "#F2A7B5", f"${T['tm_rev'][y]:.0f}bn") for y in range(2015, 2026)]
        cols = vbars(items, base_y=-2.2, height=3.6, width=0.62, gap=0.28, size=13, max_value=95)
        lab = tx("T-Mobile's revenue, $bn a year", 17, GREY_A).to_edge(UP, buff=0.8)
        mk = tx("1 April 2020: Sprint merger", 16, "#F2A7B5", bold=True).move_to([0.6, 1.6, 0])
        src = source("T-Mobile US, Forms 10-K via SEC company facts; Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> T-Mobile was the smallest of the four in 2015, with {T['tm_rev'][2015]:.0f} billion "
             "dollars of revenue. <bookmark mark='b'/> On 1 April 2020 it merged with Sprint, the third. "
             f"<bookmark mark='c'/> By 2025 it took in {T['tm_rev'][2025]:.0f} billion and served "
             f"{T['customers'] / 1e3:.0f} million customers, after buying UScellular's wireless business in August 2025.",
             base=[lab, src], steps=[VGroup(*cols[:5]), VGroup(*cols[5:6], mk), VGroup(*cols[6:])])

    def count(self):
        T = R["three"]
        items = [("T-Mobile: all customers", T["customers"] / 1e3, "#F2A7B5", f"{T['customers'] / 1e3:.1f}m"),
                 ("of which postpaid phones", get("tm30.customers") * 0 + 85.594, "#F2A7B5", "85.6m"),
                 ("Verizon Consumer: wireless retail connections", 115.903, WIRELESS, "115.9m"),
                 ("Verizon Consumer: postpaid accounts", get("vz30.accounts") / 1e3, WIRELESS, f"{get('vz30.accounts') / 1e3:.1f}m")]
        rows = hbars(items, max_value=150, x0=1.4, top=1.6, row=0.85, length=4.8, size=16, bar_h=0.42)
        lab = tx("end of 2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 of T-Mobile and Verizon", size=12)
        beat(self,
             f"<bookmark mark='a'/> T-Mobile counted {T['customers'] / 1e6 * 1e3:.0f} million customers at the end of 2025, "
             "<bookmark mark='b'/> 86 million of them on postpaid phone plans. <bookmark mark='c'/> Verizon's consumer "
             "business alone had 116 million wireless connections, <bookmark mark='d'/> in "
             f"{get('vz30.accounts') / 1e3:.1f} million accounts. In this series' reading, with nearly every adult already "
             "carrying a phone, the main way to grow is to take customers from each other.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def alike(self):
        S = R["sub"]
        rows = [["", "phone churn a month, 2025", "revenue a month per account"],
                ["Verizon", f"{get('vz30.churn'):.2f}%", f"${get('vz30.arpa'):.2f}"],
                ["AT&T", f"{get('att30.churn'):.2f}%", "not reported this way"],
                ["T-Mobile", f"{get('tm30.churn'):.2f}%", f"${get('tm30.arpa'):.2f}"]]
        t = table(rows, col_x=[-4.2, -0.4, 3.6], top=1.6, row_h=0.8, size=19,
                  colors=[None, [WIRELESS, WHITE, WHITE], ["#4F8FE6", WHITE, WHITE], ["#F2A7B5", WHITE, WHITE]])
        tag = estimate_tag("Forms 10-K for 2025; Verizon's figures are its Consumer segment's; the reading is this series'", size=12)
        beat(self,
             "Now the three are hard to tell apart. <bookmark mark='a'/> Each loses a little under one per cent of its "
             "phone customers a month, <bookmark mark='b'/> and Verizon and T-Mobile collect about a hundred and fifty "
             "dollars a month per account. In this series' reading, that is the telecom problem in a table: when the "
             "products are this alike, customers move for price, and price competition is what keeps the margin thin.",
             base=[tag, t[0], VGroup(*[t[i][0] for i in (1, 2, 3)])],
             steps=[VGroup(*[t[i][1] for i in (1, 2, 3)]), VGroup(*[t[i][2] for i in (1, 2, 3)])])

    def margins(self):
        M = R["three"]["margins"]
        ch = line_chart({"Verizon": (M["Verizon"], WIRELESS), "AT&T": (M["AT&T"], "#4F8FE6"), "T-Mobile": (M["T-Mobile"], "#F2A7B5")},
                        x=(2015, 2025), y=(-5, 30), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 10, 20, 30],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="operating profit per dollar of revenue", width=9.0, height=4.4,
                        center=(-1.2, -0.45))
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And with three instead of four, the profits converge. <bookmark mark='a'/> T-Mobile kept about "
             f"{M['T-Mobile'][2019]:.0f} cents of operating profit per dollar before the merger, and "
             f"{M['T-Mobile'][2025]:.0f} in 2025; <bookmark mark='b'/> Verizon {M['Verizon'][2025]:.0f}, AT&T "
             f"{M['AT&T'][2025]:.0f}. Three networks, each with about a fifth of its revenue as operating profit, and each "
             "spending much of that on the next network. Three is the number the American market has settled on, for "
             "now; chapter ten asks whether a fourth was ever possible.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["T-Mobile"], ch.labels["T-Mobile"]),
                                         VGroup(*[VGroup(ch.lines[k], ch.labels[k]) for k in ("Verizon", "AT&T")])])
