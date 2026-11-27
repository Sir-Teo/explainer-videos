from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.prices()
        self.made()
        self.seasons()

    def prices(self):
        P = R["prices"]
        ch = line_chart({"clothes": ({y: v for y, v in P["app"].items() if y <= 2025}, LUX),
                         "everything": ({y: v for y, v in P["all"].items() if y <= 2025}, GREY_B)},
                        x=(1990, 2025), y=(0.5, 2.6), xticks=[1990, 2000, 2010, 2020, 2025], yticks=[0.5, 1.0, 1.5, 2.0, 2.5],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="American consumer prices, 1990 = 1", width=9.6, height=4.4,
                        center=(-0.8, -0.45))
        one = DashedLine(ch.ax.c2p(1990, 1), ch.ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        hd = tx("Intermission: what clothes cost", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, CPI-U: apparel and all items (NSA), annual averages, via FRED", size=12)
        beat(self,
             "An intermission, and three pictures. First, the price of clothes. <bookmark mark='a'/> Since 1990 prices in "
             f"America, all of them together, have risen {P['all_x']:.1f} times. <bookmark mark='b'/> The price of clothes "
             f"has risen {P['app_x']:.2f} times: hardly at all. Measured against everything else, a shirt costs "
             f"{100 * (1 - P['real']):.0f} per cent less than it did in 1990, over the same years in which the sewing left "
             "America for countries where an hour of work costs far less.",
             base=[hd, ch.frame, one, src], steps=[[ch.lines["everything"], ch.labels["everything"]],
                                                   [ch.lines["clothes"], ch.labels["clothes"]]])

    def made(self):
        fred_ip = R["made"]["jobs"]
        ch = line_chart({"jobs": (fred_ip, DEPT)}, x=(1990, 2025), y=(0, 1000), xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[0, 250, 500, 750, 1000], yfmt=lambda v: f"{v:.0f}k", ylabel="American jobs making clothes",
                        width=9.6, height=4.4, center=(-0.6, -0.45), label_end=False)
        q = DashedLine(ch.ax.c2p(2005, 0), ch.ax.c2p(2005, 1000), stroke_color=PRICE, stroke_width=2)
        ql = tx("quotas end, 2005", 14, PRICE, bold=True).next_to(ch.ax.c2p(2005, 1000), RIGHT, buff=0.1).shift(DOWN * 0.2)
        y05 = fred_ip[2005]
        src = source("BLS via FRED: apparel manufacturing employment; WTO, Agreement on Textiles and Clothing", size=12)
        beat(self,
             "Second, the same story from the factory floor. <bookmark mark='a'/> American jobs making clothes fell through "
             f"the 1990s. <bookmark mark='b'/> By 2005, when the quotas ended, about {y05:.0f} thousand were left, and the fall "
             "went on after it, more slowly, because there was less left to lose.",
             base=[ch.frame, src], steps=[ch.lines["jobs"], [q, ql]])

    def seasons(self):
        H = R["hook"]
        items = [(f"Q{q}", H["q"][q][0] / 1e3, FAST if q != 4 else PRICE, f"€{H['q'][q][0] / 1e3:.1f}bn") for q in (1, 2, 3, 4)]
        bars_ = vbars(items, base_y=-2.2, height=3.6, width=1.3, gap=0.6, size=18, max_value=12)
        months = VGroup(*[tx(m, 13, GREY_B).next_to(b, DOWN, buff=0.45) for b, m in
                          zip(bars_, ("Feb-Apr", "May-Jul", "Aug-Oct", "Nov-Jan"))])
        lab = tx("Inditex's sales, each quarter of the year to January 2026", 16, GREY_A).to_edge(UP, buff=0.75)
        src = source("Inditex, FY2025 results, Annex I", size=12)
        beat(self,
             "Third, the calendar. <bookmark mark='a'/> Inditex's sales from February to April were "
             f"{H['q'][1][0] / 1e3:.1f} billion euros; from May to July, {H['q'][2][0] / 1e3:.1f}; from August to October, "
             f"{H['q'][3][0] / 1e3:.1f}. <bookmark mark='b'/> And from November to January, with Christmas and the winter "
             f"sales, {H['q'][4][0] / 1e3:.1f}. The biggest quarter by sales is the one with the lowest margin, which is what "
             "the opening of this film would lead you to expect.",
             base=[lab, src], steps=[[VGroup(*bars_[:3]), VGroup(*months[:3])], [bars_[3], months[3]]])
