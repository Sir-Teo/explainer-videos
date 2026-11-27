from __future__ import annotations

import datetime as dt

from videos.industry.industry18.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.orders()
        self.monthly()

    def orders(self):
        H = R["history"]
        o = {y: v / 1e3 for y, v in H["orders"].items() if y <= 2025}
        s = {y: v / 1e3 for y, v in H["ships"].items() if 1993 <= y <= 2025}
        d = {y: v / 1e3 for y, v in H["def_orders"].items() if y <= 2025}
        ch = line_chart({"orders": (o, PRICE), "shipments": (s, AIRBUS), "defence orders": (d, DEFENCE)}, x=(1993, 2025),
                        y=(0, 340), xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 100, 200, 300],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="US makers' aircraft and parts, $bn a year (not adjusted for inflation)",
                        width=9.6, height=4.5, center=(-0.8, -0.45), nudge={"shipments": -0.15, "defence orders": -0.2})
        ax = ch.ax
        m09 = marker(ax, 2009, o[2009], f"2009: ${o[2009]:.0f}bn", BAD, side=DOWN)
        m19 = marker(ax, 2019, o[2019], f"2019: ${o[2019]:.0f}bn", BAD, side=DOWN)
        m25 = marker(ax, 2025, o[2025], f"2025: ${o[2025]:.0f}bn", GOOD, side=LEFT)
        head_ = tx("Intermission: thirty years of American aircraft orders", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("US Census Bureau, Manufacturers' Shipments, Inventories and Orders: nondefense and defense aircraft and "
                     "parts, new orders and shipments, seasonally adjusted (via FRED: ANAPNO, ANAPVS, ADAPNO)", size=12)
        beat(self,
             "An intermission, and one picture from America's monthly survey of manufacturers: the value of new orders "
             "for civil aircraft and parts, year by year since 1993. <bookmark mark='a'/> Orders swing wildly. They "
             f"soared to {o[2007]:.0f} billion dollars in 2007 and collapsed to {o[2009]:.0f} billion in 2009, in the "
             f"financial crisis. <bookmark mark='b'/> In 2019, with the 737 MAX grounded, they fell to {o[2019]:.0f} "
             f"billion. <bookmark mark='c'/> And in 2025 they reached a record {o[2025]:.0f} billion. "
             "<bookmark mark='d'/> Now the shipments, what the factories actually delivered. They barely flinch. The "
             "backlog turns a wild market into a steady one: an airline that cancels in a bad year leaves a gap that "
             "another airline, waiting in the queue, fills. <bookmark mark='e'/> And the defence orders run steadier "
             "still, because their buyer plans in budgets, not in booms.",
             base=[ch.frame, head_, src],
             steps=[ch.lines["orders"], m09, m19, [m25, ch.labels["orders"]], [ch.lines["shipments"], ch.labels["shipments"]],
                    [ch.lines["defence orders"], ch.labels["defence orders"]]])

    def monthly(self):
        H = R["history"]
        mo = H["monthly"]
        t = lambda m: int(m[:4]) + (int(m[5:7]) - 0.5) / 12  # noqa: E731
        pts = [(t(m), v / 1e3) for m, v in sorted(mo.items())]
        pa = viz.plot_axes([2018, 2027], [-10, 65], x_length=10.0, y_length=4.4, xticks=[2018, 2020, 2022, 2024, 2026],
                           yticks=[0, 20, 40, 60], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="new orders for US civil aircraft and parts, $bn a month", size=13).move_to([-0.4, -0.45, 0])
        ax = pa.ax
        bars_ = VGroup()
        for x, v in pts:
            if x < 2018:
                continue
            h = abs(ax.c2p(x, v)[1] - ax.c2p(x, 0)[1])
            b = Rectangle(width=0.07, height=max(h, 0.01), stroke_width=0, fill_color=BAD if v < 0 else PRICE,
                          fill_opacity=0.9)
            b.move_to(ax.c2p(x, v / 2))
            bars_.add(b)
        zero = Line(ax.c2p(2018, 0), ax.c2p(2027, 0), stroke_color=GREY_B, stroke_width=1.5)
        neg = [(m, v) for m, v in mo.items() if v < 0 and m >= "2018"]
        lo = min(neg, key=lambda kv: kv[1])
        hi = max(((m, v) for m, v in mo.items() if m >= "2018"), key=lambda kv: kv[1])
        mlo = marker(ax, t(lo[0]), lo[1] / 1e3, f"{lo[0]}: -${-lo[1] / 1e3:.1f}bn", BAD, side=DOWN)
        mhi = marker(ax, t(hi[0]), hi[1] / 1e3, f"{hi[0]}: ${hi[1] / 1e3:.0f}bn", GOOD, side=LEFT)
        n_neg = len(neg)
        name = lambda m: dt.date(int(m[:4]), int(m[5:7]), 1).strftime("%B %Y")  # noqa: E731
        share = hi[1] / H["orders"][int(hi[0][:4])]
        src = source("US Census Bureau, M3 survey, via FRED (ANAPNO): nondefense aircraft and parts, new orders", size=12)
        beat(self,
             "Zoom in to single months since 2018. <bookmark mark='a'/> Each bar is one month's new orders, net of "
             f"cancellations. <bookmark mark='b'/> In {n_neg} of these months the number was below zero: more orders "
             f"cancelled than placed. The worst was {name(lo[0])}, with the 737 MAX grounded and the pandemic emptying "
             f"the skies. <bookmark mark='c'/> The best single month, {name(hi[0])}, brought {hi[1] / 1e3:.0f} billion "
             f"dollars, {100 * share:.0f} per cent of that year's orders. The order book is lumpy because airlines buy "
             "in fleets.",
             base=[pa, zero, src], steps=[bars_, mlo, mhi])
