from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Sectors(VoiceoverScene):
    def construct(self):
        card(self, 5, "Nine kinds of building", "Are offices, malls, warehouses and towers one business?",
             "Chapter five. Nine kinds of building. Property is not one industry but several, which happen to share a "
             "formula.", lit=("unit", "dollar", "moat"))
        self.kinds()
        self.margins()
        self.occupancy()
        self.why()

    def kinds(self):
        g = VGroup(VGroup(draw.office_tower(0.8), tx("offices", 15, OFFICE)).arrange(DOWN, buff=0.15),
                   VGroup(draw.warehouse(1.8), tx("warehouses", 15, SHED)).arrange(DOWN, buff=0.15),
                   VGroup(draw.mall(1.8), tx("malls and shops", 15, SHOP)).arrange(DOWN, buff=0.15),
                   VGroup(draw.house(1.0), tx("flats", 15, GROUP_COL["homes"])).arrange(DOWN, buff=0.15),
                   VGroup(draw.cell_tower(1.6), tx("phone towers", 15, GROUP_COL["towers"])).arrange(DOWN, buff=0.15),
                   VGroup(VGroup(draw.server_rack(1.2), draw.server_rack(1.2)).arrange(RIGHT, buff=0.08),
                          tx("data centres", 15, GROUP_COL["data"])).arrange(DOWN, buff=0.15))
        g.arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to([0, 0.2, 0])
        if g.width > 13:
            g.scale_to_fit_width(13)
        beat(self,
             "Every one of these is a building let to tenants and valued as income over a rate. <bookmark mark='a'/> Offices "
             "and <bookmark mark='b'/> warehouses, <bookmark mark='c'/> malls and shops, <bookmark mark='d'/> blocks of "
             "flats, <bookmark mark='e'/> the masts that carry phone networks, <bookmark mark='f'/> and the halls full of "
             "servers. Their tenants, their leases and their costs are as different as their shapes.",
             base=[], steps=list(g))

    def margins(self):
        S = sorted(R["sectors"], key=lambda s: -s["margin"])
        items = [(f"{s['name']} ({s['co']})", 100 * s["margin"], GROUP_COL[{'warehouses': 'industrial', 'malls': 'retail',
                  'net-leased shops': 'retail', 'offices': 'office', 'flats': 'homes', 'self-storage': 'storage',
                  'phone towers': 'towers', 'data centres': 'data', 'senior housing': 'health'}[s['name']]], f"{100 * s['margin']:.0f}%")
                 for s in S]
        rows = hbars(items, max_value=50, x0=0.4, top=2.4, row=0.52, length=5.6, size=15, bar_h=0.34)
        lab = tx("net income per dollar of revenue, median of 2021-2025, the largest listed owner of each kind", 15, GREY_A).to_edge(UP, buff=0.45)
        src = source("Forms 10-K via SEC company facts", size=12)
        top, bot = S[0], S[-1]
        beat(self,
             "Here is what one large owner of each kind kept of each dollar of revenue over the last five years. "
             f"<bookmark mark='a'/> At the top, self-storage, malls and warehouses: Public Storage, Simon and Prologis kept "
             "between forty-five and forty-eight cents, though Simon's figure includes gains on things it sold. "
             f"<bookmark mark='b'/> Flats, towers and single-tenant shops, between eighteen and thirty-seven. "
             f"<bookmark mark='c'/> At the bottom, data centres, offices and senior housing, under ten: "
             f"{bot['co']} kept {100 * bot['margin']:.0f} cents.",
             base=[lab, src], steps=[VGroup(*rows[:3]), VGroup(*rows[3:6]), VGroup(*rows[6:])])

    def occupancy(self):
        c = stat_cards([(f"{get('o.occ'):.1f}%", "Realty Income's single-tenant properties", INCOME),
                        (f"{get('spg.occ'):.1f}%", "Simon's malls and outlets", SHOP),
                        (f"{get('pld.occ'):.1f}%", "Prologis's warehouses", SHED),
                        (f"{get('bxp.occ'):.1f}%", "BXP's offices", OFFICE)], y=0.2, size=38, span=12.4)
        lab = tx("share let, end of 2025", 18, GREY_A).move_to([0, 1.8, 0])
        src = source("Forms 10-K for 2025 of Realty Income, Simon Property Group, Prologis and BXP", size=12)
        beat(self,
             "And how full they are. <bookmark mark='a'/> Realty Income's single-tenant buildings were "
             f"{get('o.occ'):.1f} per cent let at the end of 2025. <bookmark mark='b'/> Simon's malls and outlets "
             f"{get('spg.occ'):.1f}. <bookmark mark='c'/> Prologis's warehouses {get('pld.occ'):.1f}. "
             f"<bookmark mark='d'/> BXP's offices, some of the best in America, {get('bxp.occ'):.1f}: the one kind of building "
             "on this list whose tenants found they needed less of it.",
             base=[lab, src], steps=list(c))

    def why(self):
        g = VGroup(tx("Why the margins differ", 22, WHITE, bold=True),
                   tx("storage, malls, warehouses: the tenant does most of the work; costs are low per dollar of rent", 17, SHED),
                   tx("towers: one mast, several tenants; most of each new tenant's rent is profit", 17, GROUP_COL["towers"]),
                   tx("data centres and senior housing: power, cooling, nurses and meals; an operating business in a building", 17,
                      GROUP_COL["data"]),
                   tx("offices: costly to run, to fit out for each tenant, and to finance; and emptier since 2020", 17, OFFICE)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading of the margins", size=12)
        beat(self,
             "Why so different? In this series' reading, <bookmark mark='a'/> a storage unit, a mall or a warehouse needs "
             "little from its landlord once it is built: the tenant does the work and often pays the costs. "
             "<bookmark mark='b'/> A tower earns again from every network on the same mast. <bookmark mark='c'/> Data centres "
             "and senior homes are operating businesses inside buildings: power and cooling in one, nurses and meals in the "
             "other, and their margins look like those of the businesses they are. <bookmark mark='d'/> And offices are "
             "expensive to run, to refit for each new tenant, and to finance, and have been emptier since 2020.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
