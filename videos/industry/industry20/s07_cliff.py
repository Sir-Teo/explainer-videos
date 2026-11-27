from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Cliff(VoiceoverScene):
    def construct(self):
        card(self, 6, "The cliff", "What happens to the price when the copies arrive?",
             "Chapter six. The cliff. What happens to the price of a medicine when the copies arrive?", lit=("dollar", "change"))
        self.generics()
        self.approvals()
        self.lipitor()

    def approvals(self):
        G = R["generics"]
        items = [(str(y), v, GENERIC, f"{v}") for y, v in sorted(G.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.4, width=1.3, gap=0.9)
        vials = VGroup(*[draw.vial(0.5, GENERIC).move_to([-5.8 + 0.45 * (k % 4), 2.0 - 0.55 * (k // 4), 0]) for k in range(8)])
        src = source("US Food and Drug Administration: generic drug applications fully approved, 2021-2024", size=12)
        beat(self,
             "And the copies keep coming. <bookmark mark='a'/> The FDA fully approved "
             f"{G[2021]} generic drug applications in 2021 and {G[2022]} in 2022, <bookmark mark='b'/> {G[2023]} in 2023 and "
             f"{G[2024]} in 2024: more than ten for every new medicine. Generic makers compete on the cost of making "
             "the pill and on being first to file, not on discovery.",
             base=[vials, head("Generic drug applications approved by the FDA"), src],
             steps=[VGroup(bars_[0], bars_[1]), VGroup(bars_[2], bars_[3])])

    def generics(self):
        C = R["cliff"]
        f = C["fda"]
        items = [("brand, before", 100, BRAND, "100"), ("1 generic maker", 100 - f[1], GENERIC, f"{100 - f[1]}"),
                 ("2 makers", 100 - f[2], GENERIC, f"{100 - f[2]}"), ("4 makers", 100 - f[4], GENERIC, f"{100 - f[4]}"),
                 ("6 or more", 100 - f[6], GENERIC, f"under {100 - f[6]}")]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.3, gap=0.9)
        hd = tx("generic price as a share of the brand's price before competition (average manufacturer prices)", 15, GREY_A).to_edge(UP, buff=0.9)
        tabs = VGroup(*[draw.tablet(0.16).move_to([4.6 + 0.4 * (k % 6), 2.0 - 0.4 * (k // 6), 0]) for k in range(12)])
        src = source("US Food and Drug Administration, Generic Competition and Drug Prices (2019)", size=12)
        beat(self,
             "When exclusivity ends, other companies may sell the same molecule, once they show the regulator it works "
             "the same way. The FDA studied what happens to prices. <bookmark mark='a'/> Start with the brand's price "
             f"before competition as one hundred. <bookmark mark='b'/> With one generic maker, the generic price is "
             f"{f[1]} per cent lower. <bookmark mark='c'/> With two, {f[2]} per cent. <bookmark mark='d'/> With four, "
             f"{f[4]} per cent, <bookmark mark='e'/> and with six or more, more than {f[6]} per cent lower. Across all "
             f"the drugs in the study, the median generic sold for {C['median']} per cent of the brand's old price. A pill "
             "that sold for dollars sells for cents, because making it was always cheap; the price had been paying for "
             "the discovery, not the manufacture.",
             base=[hd, tabs, src], steps=list(bars_))

    def lipitor(self):
        C = R["cliff"]
        lip = C["lipitor"]
        tl = viz.plot_axes([2010.9, 2012.6], [0, 1], x_length=10.5, y_length=1.2, xticks=[2011, 2012],
                           xfmt=lambda v: f"{int(v)}", grid=False, size=14).move_to([0, 1.6, 0])
        ax = tl.ax
        evs = [(2011.45, "June 2011: Japan", GREY_A), (2011.9, "November 2011: the US", BAD), (2012.2, "March-May 2012: Europe", GREY_A),
               (2012.37, "May 2012: US generics arrive", PRICE)]
        marks = VGroup(*[marker(ax, x, 0.5, lab, col, side=UP if i % 2 == 0 else DOWN, size=13) for i, (x, lab, col) in enumerate(evs)])
        items = [(str(y), v / 1e3, BRAND if y < 2012 else GENERIC, f"${v / 1e3:.1f}bn") for y, v in sorted(lip.items())]
        bars_ = vbars(items, base_y=-2.6, height=2.4, width=1.2, gap=0.8, x0=-1.5)
        src = source("Pfizer Inc., Form 10-K 2012 (Exhibit 13): loss of exclusivity dates and Lipitor revenues", size=12)
        beat(self,
             "Lipitor shows the cliff in real accounts. <bookmark mark='a'/> It lost its exclusivity country by country: "
             "Japan in June 2011, America in November, much of Europe the next spring. <bookmark mark='b'/> In America, "
             "competition from several generic makers began in May 2012, six months after exclusivity ended. "
             f"<bookmark mark='c'/> Pfizer's Lipitor sales went from "
             f"{lip[2011] / 1e3:.1f} billion dollars to {lip[2012] / 1e3:.1f} billion in a year. What a company needs, "
             "long before the date, is other drugs to take the old one's place.",
             base=[tl, src], steps=[VGroup(*marks[:3]), marks[3], bars_])
