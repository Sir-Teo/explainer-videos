from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.staggers()
        self.ratios()
        self.firms()
        self.title()

    def staggers(self):
        q = quote(["'earnings by the railroad industry are the lowest of any transportation mode and are insufficient",
                   "to generate funds for necessary capital improvements'"],
                  "the Staggers Rail Act, Public Law 96-448, section 2, 14 October 1980", size=19).move_to([0, 1.7, 0])
        tr = draw.train(7, 1.0, kinds=("hopper", "box", "tank", "well"),
                        colors=("#B58CFF", "#7BD88F", "#C9D3E0", "#E8554E")).move_to([0, -1.4, 0])
        src = source("Public Law 96-448, 94 Stat. 1895 (govinfo)", size=12)
        beat(self,
             "In October 1980 the United States Congress wrote down what it thought of its railways. <bookmark mark='a'/> "
             "'Earnings by the railroad industry,' the law says, 'are the lowest of any transportation mode, and are "
             "insufficient to generate funds for necessary capital improvements.' It expected a shortfall of sixteen to "
             "twenty billion dollars by 1985. <bookmark mark='b'/> So it set the railways free to price their own "
             "services, and the industry it described has become something very different.",
             base=[src], steps=[q, tr])

    def ratios(self):
        H = R["hook"]["ors"]
        cols = {"Union Pacific": RAIL, "BNSF": "#E8C77A", "CSX": "#D9A441", "Norfolk Southern": "#BFA36A",
                "Knight-Swift": TRUCK, "Werner": "#F08A84"}
        ch = line_chart({k: (H[k], c) for k, c in cols.items()}, x=(2009, 2025), y=(50, 100),
                        xticks=[2009, 2013, 2017, 2021, 2025], yticks=[50, 60, 70, 80, 90, 100], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="operating ratio: costs per dollar of revenue (lower is better)", width=8.8, height=4.4,
                        center=(-1.3, -0.45))
        src = source("Forms 10-K via SEC company facts (operating expenses over revenue)", size=12)
        rail = [k for k in cols if k not in ("Knight-Swift", "Werner")]
        beat(self,
             "Railways measure themselves by the operating ratio: how many cents of every dollar of revenue go on running "
             "the business. Lower is better. <bookmark mark='a'/> In 2009 America's four big railways spent about "
             f"seventy-five cents of each dollar. By 2025 Union Pacific spent {H['Union Pacific'][2025]:.1f}, keeping about "
             "forty cents in every dollar before interest and tax. <bookmark mark='b'/> Now the lorries. Knight-Swift, "
             f"which runs 'one of the country's largest truckload fleets', spent {H['Knight-Swift'][2025]:.0f} cents of each dollar in 2025, "
             f"Werner {H['Werner'][2025]:.1f}.",
             base=[ch.frame, src], steps=[VGroup(*[VGroup(ch.lines[k], ch.labels[k]) for k in rail]),
                                         VGroup(*[VGroup(ch.lines[k], ch.labels[k]) for k in ("Knight-Swift", "Werner")])])

    def firms(self):
        H = R["hook"]
        c = stat_cards([("4", "large freight railways in the United States", RAIL),
                        (f"{H['carriers']:,.0f}", "trucking companies for hire across state lines", TRUCK),
                        (f"{H['one']:,.0f}", "of them with one truck", TRUCK)], y=0.6, size=40, span=12.4)
        trucks = VGroup(*[draw.semi(1.3, cab_color=TRUCK) for _ in range(6)]).arrange(RIGHT, buff=0.25).move_to([0, -1.8, 0])
        src = source("FMCSA Company Census File, active interstate for-hire carriers, counted by this series on 27 November 2026", size=12)
        beat(self,
             "And count the firms. <bookmark mark='a'/> Freight rail in the United States is mostly four companies, each "
             "with a region of its own. <bookmark mark='b'/> The government's register of trucking companies that carry "
             f"other people's goods across state lines lists {H['carriers']:,.0f} active firms. <bookmark mark='c'/> More "
             f"than half of them, {H['one']:,.0f}, own a single truck.",
             base=[trucks, src], steps=[c[0], c[1], c[2]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-nine: rail, trucks and parcels. Why is one freight industry a set "
                            "of regional monopolies, and the next a market of half a million firms?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
