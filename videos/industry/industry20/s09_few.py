from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Few(VoiceoverScene):
    def construct(self):
        card(self, 7, "Companies of a few products", "What happens to a company whose biggest drug has a date?",
             "Chapter seven. Companies of a few products. What happens to a company when half its sales come from one "
             "medicine with an end date?", lit=("moat", "change"))
        self.keytruda()
        self.pfizer()
        self.dates()

    def pfizer(self):
        pf = R["pfizer"]
        items = [(str(y), v, BAD if y in (2021, 2022) else BRAND, f"{v:.0f}") for y, v in sorted(pf.items()) if y >= 2015]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=0.7, gap=0.25, size=13)
        src = source("Pfizer Inc., Forms 10-K via SEC company facts: revenue, $bn", size=12)
        beat(self,
             "Even the biggest company's sales can swing. <bookmark mark='a'/> Pfizer's revenue was around forty to "
             f"fifty billion dollars a year before the pandemic. <bookmark mark='b'/> In 2021 and 2022, the pandemic "
             f"years, it jumped to {pf[2021]:.0f} and then {pf[2022]:.0f} billion. <bookmark mark='c'/> In 2023 it "
             f"fell back to {pf[2023]:.0f}. A product can make a company, briefly, twice its size, and the drop afterwards "
             "looks like a cliff even without a patent ending.",
             base=[head("Pfizer's revenue, $bn"), src], steps=[VGroup(*bars_[:6]), VGroup(*bars_[6:8]), VGroup(*bars_[8:])])

    def keytruda(self):
        H = R["hook"]
        share = H["key_share"] / 100
        pie = VGroup()
        ang = share * TAU
        a = AnnularSector(inner_radius=0.9, outer_radius=1.8, angle=ang, start_angle=PI / 2, color=BRAND, fill_opacity=0.9).move_to([-3.4, 0.2, 0])
        b = AnnularSector(inner_radius=0.9, outer_radius=1.8, angle=TAU - ang, start_angle=PI / 2 + ang, color=GREY_B, fill_opacity=0.35)
        b.move_arc_center_to(a.get_arc_center())
        pie.add(a, b)
        lab = VGroup(tx(f"{H['key_share']}%", 30, BRAND, bold=True), tx("Keytruda", 16, BRAND)).arrange(DOWN, buff=0.05).move_to(a.get_arc_center())
        facts = VGroup(tx(f"Keytruda, 2025: ${H['keytruda'] / 1e3:.1f}bn of sales", 19, WHITE, bold=True),
                       tx(f"main US patent: {H['key_us']}; Europe 2031; Japan 2032-33", 17, GREY_A),
                       tx(f"Lilly: Mounjaro and Zepbound, {H['lly_share']}% of 2025 revenue", 17, LAB, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.6, 0.4, 0])
        src = source("Merck & Co., Inc. and Eli Lilly and Company, Forms 10-K 2025", size=12)
        beat(self,
             "Take Merck. <bookmark mark='a'/> In 2025, "
             f"{H['key_share']} per cent of its sales came from Keytruda, a cancer immunotherapy, "
             f"{H['keytruda'] / 1e3:.1f} billion dollars. <bookmark mark='b'/> Its main American patent runs out in "
             f"{H['key_us']}; in Europe, 2031, and in Japan, 2032 to 2033, so the cliff comes country by country, as "
             "Lipitor's did. Merck has also won approval in America for Keytruda Qlex, the same antibody given as an "
             "injection under the skin rather than a drip, a new form that patients may move to before the old one's date. "
             "<bookmark mark='c'/> And Lilly took {H['lly_share']} per cent of its revenue from one molecule "
             "under two brand names. The biggest companies in the industry are, at any moment, a few drugs and a calendar, "
             "and investors watch the calendar as closely as the sales.",
             base=[src], steps=[[pie, lab], facts[:2], facts[2]])

    def dates(self):
        H = R["hook"]
        pa = viz.plot_axes([2010, 2032], [0, 1], x_length=11.0, y_length=1.2, xticks=[2011, 2016, 2021, 2026, 2031],
                           xfmt=lambda v: f"{int(v)}", grid=False, size=14).move_to([0, 0.6, 0])
        ax = pa.ax
        m1 = marker(ax, 2011, 0.5, "Lipitor, US, 2011", GENERIC, side=UP)
        m2 = marker(ax, H["key_us"], 0.5, f"Keytruda, US, {H['key_us']}", BRAND, side=UP)
        now = marker(ax, 2026.9, 0.5, "today", PRICE, side=DOWN)
        q = tx("The way out is the pipeline: new drugs, bought or invented, before the date.", 19, WHITE, bold=True).move_to([0, -1.6, 0])
        src = source("Pfizer Inc., Form 10-K 2012; Merck & Co., Inc., Form 10-K 2025", size=12)
        beat(self,
             "Put the dates on one line. <bookmark mark='a'/> Lipitor's American exclusivity ended in 2011. "
             f"<bookmark mark='b'/> Keytruda's main patent ends in {H['key_us']}, <bookmark mark='c'/> a little over a "
             "year from now. <bookmark mark='d'/> A company in this position spends the years before the date building "
             f"or buying the drugs that will replace it. One way is to buy them: in January 2026 Merck acquired Cidara, a "
             f"biotech company with an experimental drug, for about {H['cidara']:.1f} billion dollars.",
             base=[pa, src], steps=[m1, m2, now, q])
