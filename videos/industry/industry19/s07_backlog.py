from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Backlog(VoiceoverScene):
    def construct(self):
        card(self, 6, "Reading the cycle: backlog, price and tariffs", "How do you tell where a machine maker is in its cycle?",
             "Chapter six. Reading the cycle. Three numbers tell you where a machine maker stands: its orders against "
             "its shipments, its backlog, and its prices against its costs.", lit=("change", "dollar"))
        self.btb()
        self.bridge()
        self.power()
        self.tariffs()

    def power(self):
        B = R["backlog"]
        items = [("2024", B["pe24"], GREY_B, f"${B['pe24']:.1f}bn"), ("2025", B["pe"], BLUE, f"${B['pe']:.1f}bn")]
        bars_ = vbars(items, base_y=-2.4, height=3.6, width=1.4, gap=1.0, x0=-4.2)
        srv = draw.server_rack(1.4) if hasattr(draw, "server_rack") else VGroup()
        srv.move_to([1.4, 0.4, 0])
        q3 = VGroup(tx(f"third quarter of 2026: ${B['pe_q3']:.1f}bn, up 18%", 18, BLUE, bold=True),
                    tx("'primarily in data center applications'", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.8, -1.6, 0])
        src = source("Caterpillar Inc., Form 10-K 2025 and Form 10-Q for the third quarter of 2026: Power & Energy", size=12)
        beat(self,
             "Where is the boom coming from? <bookmark mark='a'/> Caterpillar's Power and Energy segment, its engines and "
             f"turbines, sold {B['pe24']:.1f} billion dollars in 2024 <bookmark mark='b'/> and {B['pe']:.1f} billion in "
             "2025. <bookmark mark='c'/> Data centres need electricity, and Caterpillar's report says its sales of large "
             "engines grew primarily for data centre applications. <bookmark mark='d'/> In the third quarter "
             f"of 2026 the segment sold {B['pe_q3']:.1f} billion dollars, up eighteen per cent, and Caterpillar named "
             "data centres as a main reason. Its largest segment is now power, not bulldozers.",
             base=[head("Caterpillar's Power & Energy sales"), src], steps=[bars_[0], bars_[1], srv, q3])

    def btb(self):
        B = R["backlog"]
        b = {y: v for y, v in B["btb"].items() if y <= 2025}
        ch = line_chart({"book-to-bill": (b, PRICE)}, x=(1993, 2025), y=(0.85, 1.1), xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025],
                        yticks=[0.9, 1.0, 1.1], yfmt=lambda v: f"{v:.2f}", ylabel="US machinery makers: orders / shipments, by year",
                        width=9.6, height=4.2, center=(-0.6, -0.45), label_end=False)
        ax = ch.ax
        one = DashedLine(ax.c2p(1993, 1), ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        above = tx("above 1: the backlog grows", 15, GOOD, bold=True).move_to(ax.c2p(2000, 1.08))
        below = tx("below 1: the factories eat into it", 15, BAD, bold=True).move_to(ax.c2p(2001, 0.88))
        m09 = marker(ax, 2009, b[2009], f"2009: {b[2009]:.2f}", BAD, side=RIGHT)
        src = source("US Census Bureau, M3 survey: machinery new orders and shipments (via FRED: A33SNO, A33SVS)", size=12)
        beat(self,
             "First, book-to-bill: a year's new orders divided by what was shipped. <bookmark mark='a'/> Above one, the "
             "makers are taking orders faster than they fill them, and the backlog grows. <bookmark mark='b'/> Below one, "
             "they are living off orders taken earlier. <bookmark mark='c'/> For America's machinery makers it fell to "
             f"{b[2009]:.2f} in 2009, the deepest since this record began, and has stayed close to one since.",
             base=[ch.frame, one, src], steps=[[ch.lines["book-to-bill"], above], below, m09])

    def bridge(self):
        B = R["backlog"]
        steps_ = [("2024", B["op24"], GREY_B, True), ("more machines sold", B["volume"], GOOD, False),
                  ("lower prices", B["price"] / 1e3, BAD, False), ("higher costs, mostly tariffs", B["mfg"], BAD, False),
                  ("2025", B["op25"], MACHINE, True)]
        s = 0.28
        x0, base = -5.2, -2.4
        bars_ = VGroup()
        run = 0.0
        for i, (lab, v, col, total) in enumerate(steps_):
            x = x0 + 2.55 * i
            if total:
                lo, hi = 0.0, v
                run = v
            else:
                lo, hi = (run, run + v) if v >= 0 else (run + v, run)
                run += v
            r_ = Rectangle(width=1.4, height=max((hi - lo) * s, 0.03), stroke_width=0, fill_color=col, fill_opacity=0.9)
            r_.move_to([x, base + (lo + hi) / 2 * s, 0])
            r_.grow = DOWN if (total or v >= 0) else UP
            val = tx(("" if total else ("+" if v >= 0 else "-")) + f"${abs(v):.2f}bn", 15, col, bold=True).next_to(r_, UP, buff=0.08)
            name = tx(lab, 14, GREY_A).move_to([x, base - 0.3, 0])
            if name.width > 2.3:
                name.scale_to_fit_width(2.3)
            bars_.add(VGroup(r_, val, name))
        src = source("Caterpillar Inc., Form 10-K 2025: consolidated operating profit comparison", size=12)
        beat(self,
             "Second, price against cost. Here is how Caterpillar's operating profit moved from 2024 to 2025. "
             f"<bookmark mark='a'/> It started at {B['op24']:.1f} billion dollars. <bookmark mark='b'/> Selling more "
             f"machines added {B['volume']:.1f} billion. <bookmark mark='c'/> But Caterpillar cut its prices, which cost "
             f"{-B['price'] / 1e3:.1f} billion, <bookmark mark='d'/> and its manufacturing costs rose by "
             f"{-B['mfg']:.1f} billion, mostly from new tariffs on what it imports. <bookmark mark='e'/> Profit fell to "
             f"{B['op25']:.1f} billion in a year of record sales.",
             base=[head("Caterpillar's operating profit, 2024 to 2025"), src], steps=list(bars_))

    def tariffs(self):
        B = R["backlog"]
        rows = VGroup(
            tx(f"backlog: ${B['cat'][0]:.0f}bn (end 2024), ${B['cat'][1]:.0f}bn (end 2025), ${B['cat'][2]:.0f}bn (September 2026)", 18, MACHINE, bold=True),
            tx(f"third-quarter 2026 sales: ${B['q3']:.1f}bn, up 17%", 18, WHITE),
            tx("20 February 2026: the Supreme Court rules the IEEPA tariffs unauthorized", 18, WHITE),
            tx(f"what those tariffs had cost Caterpillar: about ${B['ieepa']:.1f}bn, now being reclaimed", 18, GOOD, bold=True),
            tx(f"tariffs still expected to cost about ${B['tariff']:.1f}bn in 2026, before reclaims", 18, BAD, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.1, 0])
        for r_ in rows:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        stamp = as_of("as of 30 September 2026")
        src = source("Caterpillar Inc., Form 10-K 2025 and Form 10-Q for the third quarter of 2026", size=12)
        beat(self,
             "Third, the backlog, and where it is heading. <bookmark mark='a'/> Caterpillar's firm orders went from "
             f"{B['cat'][0]:.0f} billion dollars to {B['cat'][2]:.0f} billion in under two years. <bookmark mark='b'/> In "
             "the third quarter of 2026 its sales rose seventeen per cent. <bookmark mark='c'/> And the tariffs moved: in "
             "February 2026 the Supreme Court ruled that tariffs imposed under an emergency powers law were unauthorized. "
             f"<bookmark mark='d'/> Those had cost Caterpillar about {B['ieepa']:.0f} billion dollars, and it began "
             "reclaiming them. <bookmark mark='e'/> Other tariffs remain: it still expects about "
             f"{B['tariff']:.1f} billion dollars of tariff costs in 2026. For a machine maker, a tariff on steel and parts "
             "is a cost it must pass on in price, or eat. In 2025 Caterpillar ate much of it: its prices fell while its "
             "costs rose, and a record year in sales became a weaker year in profit.",
             base=[stamp, src], steps=list(rows))
