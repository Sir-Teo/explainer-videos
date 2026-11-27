from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Liner(VoiceoverScene):
    def construct(self):
        card(self, 5, "Liners and the lessors", "Who runs the container network, and who owns the ships?",
             "Chapter five. Liners and the lessors. A container line runs ships on fixed timetables, like a bus company of "
             "the oceans, and it often does not own the buses.", lit=("moat", "dollar"))
        self.three()
        self.fleet()
        self.zones()
        self.margins()
        self.merger()

    def three(self):
        L = R["liner"]
        parts = [("MSC, Maersk and CMA CGM", L["top3"] / 100, BOX), ("every other line", 1 - L["top3"] / 100, ALL)]
        bar = viz.bar_split(parts, 1.0, width=11.4, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.1f}%", 22, c, bold=True), tx(n, 15, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        vessel = VGroup(draw.ship(2.0), draw.ship(2.0), draw.ship(2.0)).arrange(RIGHT, buff=0.4).move_to([0, 2.6, 0])
        src = source("Alphaliner, as quoted in ZIM's Forms 20-F for 2023 and 2025", size=12)
        beat(self,
             "Who runs the network? <bookmark mark='a'/> At the end of 2025 three companies, MSC of Switzerland, Maersk of "
             f"Denmark and CMA CGM of France, controlled {L['top3']:.1f} per cent of the world's container ship capacity, up "
             f"from {L['top3_23']:.1f} per cent two years before. <bookmark mark='b'/> Everyone else shared the rest. Lines "
             "share ships with each other in alliances, so a box booked with one may ride on another's vessel.",
             base=[vessel, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]]])

    def fleet(self):
        L = R["liner"]
        owned = int(L["owned"])
        total = int(L["ships"])
        g = VGroup(*[draw.ship(0.55) for _ in range(total)]).arrange_in_grid(rows=8, buff=(0.08, 0.12)).move_to([-1.6, -0.2, 0])
        if g.width > 8:
            g.scale_to_fit_width(8)
        for i, sh in enumerate(g):
            if i >= owned:
                sh.set_opacity(0.35)
        c = stat_cards([(f"{owned}", "owned by ZIM", BOX), (f"{total - owned}", "chartered in from shipowners", ALL)], y=0.4, size=40, span=3.4)
        c.arrange(DOWN, buff=0.6).move_to([5.0, 0.2, 0])
        src = source("ZIM Integrated Shipping Services, Form 20-F for 2025", size=12)
        beat(self,
             f"And who owns the ships? <bookmark mark='a'/> ZIM operated {total} ships at the end of 2025. "
             f"<bookmark mark='b'/> It owned {owned} of them. <bookmark mark='c'/> The other {total - owned} it chartered in, "
             "rented from shipowners by the month or for years at a time, most of them on charters with more than a year to "
             "run.",
             base=[src], steps=[g, c[0], c[1]])

    def zones(self):
        L = R["liner"]
        Z = L["zones"]
        items = [(k, v, BAD if v > 1800 else (RATE if v > 1200 else GOOD), f"${v:,.0f}") for k, v in Z.items()]
        rows = hbars(items, max_value=2100, x0=-0.6, top=1.6, row=0.75, length=6.2, size=17, bar_h=0.45)
        lab = tx("ZIM: average freight per TEU by trade, 2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("ZIM Integrated Shipping Services, Form 20-F for 2025", size=12)
        beat(self,
             "A line also sells many routes at many prices. <bookmark mark='a'/> In 2025 ZIM's boxes between Asia and the "
             f"Mediterranean, through Suez or round Africa, paid {Z['Cross-Suez']:,.0f} dollars a TEU, and across the Pacific "
             f"{Z['Pacific']:,.0f}, the trade where it carried most, {L['pacific_teu']:,.0f} thousand TEU. "
             f"<bookmark mark='b'/> Within Asia, {Z['Intra-Asia']:,.0f}: short voyages, many rivals. The long routes through "
             "the narrow places paid most.",
             base=[lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:])])

    def margins(self):
        L = R["liner"]
        series = {"ZIM, the line": ({y: 100 * v for y, v in L["zim_margin"].items()}, BOX)}
        cols = {"Global Ship Lease": GOOD, "Costamare": PORT}
        for k, col in cols.items():
            series[k + ", a lessor"] = ({y: 100 * v for y, v in L["lessors"][k].items()}, col)
        ch = line_chart(series, x=(2019, 2025), y=(-60, 60), xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[-60, -30, 0, 30, 60],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="net income per dollar of revenue", width=9.0, height=4.4,
                        center=(-1.2, -0.45), nudge={"Costamare, a lessor": -0.25})
        zero = DashedLine(ch.ax.c2p(2019, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        src = source("ZIM, Global Ship Lease and Costamare, Forms 20-F via SEC company facts", size=12)
        z = L["zim_margin"]
        beat(self,
             "Renting ships to the lines is a different business from running them. <bookmark mark='a'/> ZIM's margin swung "
             f"from {100 * z[2021]:.0f} per cent of revenue in 2021 to a loss of {abs(100 * z[2023]):.0f} per cent in 2023. "
             "<bookmark mark='b'/> Global Ship Lease and Costamare, which own container ships and charter them to lines on "
             "fixed rates for years, kept between about a third and a half of each dollar from 2022 to 2025, through the bust "
             "of 2023 as well. The line takes the freight market's risk; the lessor takes the line's credit.",
             base=[ch.frame, zero, src], steps=[[ch.lines["ZIM, the line"], ch.labels["ZIM, the line"]],
                                                [ch.lines[k] for k in series if k != "ZIM, the line"] + [ch.labels[k] for k in series if k != "ZIM, the line"]])

    def merger(self):
        L = R["liner"]
        q = quote(["'On February 16, 2026, ZIM announced that it entered into a merger agreement with Hapag-Lloyd, under which",
                   "Hapag-Lloyd will acquire ZIM for $35.00 per share in cash.'"], "ZIM, third-quarter 2026 results (Form 6-K)", size=17).move_to([0, 1.6, 0])
        steps = bullets(["approved by ZIM's shareholders on 30 April 2026",
                         "needs regulators' approval, including the State of Israel's under its 'Golden Share'",
                         "the original application to Israel was terminated; Hapag-Lloyd is to submit a new one",
                         "targeted to close in the first quarter of 2027"], size=18).move_to([0, -0.9, 0])
        src = source("ZIM Integrated Shipping Services, Form 6-K of 18 November 2026", size=12)
        beat(self,
             "And the lines are still consolidating. <bookmark mark='a'/> In February 2026 the German line Hapag-Lloyd "
             f"agreed to buy ZIM for {L['hapag']:.0f} dollars a share in cash. <bookmark mark='b'/> ZIM's shareholders "
             "approved it in April. It still needs regulators, among them the State of Israel, which holds a special 'golden "
             "share' in ZIM; the original application to Israel was terminated, and the deal is aimed to close early in 2027. "
             "Chapter ten makes a call on it.",
             base=[src], steps=[q, steps])
