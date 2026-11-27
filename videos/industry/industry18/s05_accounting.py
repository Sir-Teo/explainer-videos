from __future__ import annotations

import math

from videos.industry.industry18.common import *  # noqa: F403


class Accounting(VoiceoverScene):
    def construct(self):
        card(self, 4, "Program accounting", "How do you report profit on a bet that pays back in fifteen years?",
             "Chapter four. Program accounting: how a maker reports profit on a bet that takes fifteen years to pay back, "
             "and what happens when the bet goes wrong.", lit=("dollar",))
        self.average()
        self.quantities()
        self.reach()
        self.losses()

    def average(self):
        A = R["accounting"]
        P = R["programme"]
        u = A["unit_lin"]
        pa = viz.plot_axes([0, 1500], [0, 300], x_length=9.6, y_length=4.3, xticks=[0, 500, 1000, 1500],
                           yticks=[0, 100, 200, 300], xfmt=lambda v: f"{int(v):,}", yfmt=lambda v: f"${v:.0f}m",
                           ylabel="cost of the n-th aircraft (the Works), with the programme's average", size=13).move_to([-0.5, -0.45, 0])
        ax = pa.ax
        pts = [(n, min(c, 300)) for n, c in sorted(u.items())]
        curve = poly(ax, pts, ENGINE, 4)
        avg = A["avg"]
        cross = (P["first"] / avg) ** (1 / -math.log2(P["learning"]))
        line = VGroup(DashedLine(ax.c2p(0, avg), ax.c2p(1500, avg), stroke_color=PRICE, stroke_width=2, dash_length=0.08),
                      tx(f"average over 1,500 aircraft: ${avg:.0f}m", 14, PRICE, bold=True).next_to(ax.c2p(1200, avg), UP, buff=0.12))
        above = [(n, min(c, 300)) for n, c in sorted(u.items()) if n <= cross]
        below = [(n, c) for n, c in sorted(u.items()) if n >= cross]
        red = Polygon(*[ax.c2p(n, c) for n, c in above], ax.c2p(above[-1][0], avg), ax.c2p(above[0][0], avg),
                      stroke_width=0, fill_color=BAD, fill_opacity=0.45)
        green = Polygon(*[ax.c2p(n, c) for n, c in below], ax.c2p(below[-1][0], avg), ax.c2p(below[0][0], avg),
                        stroke_width=0, fill_color=GOOD, fill_opacity=0.45)
        lr = VGroup(tx("cost above the average: kept on the balance", 14, BAD, bold=True),
                    tx("sheet as 'deferred production costs'", 14, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(ax.c2p(700, 190))
        lg = tx("cost below the average: pays the deferral back", 14, GOOD, bold=True).next_to(ax.c2p(1000, avg), DOWN, buff=0.5)
        dpc = tx(f"the 777X's deferred production costs: ${A['dpc'] / 1e3:.1f}bn at 30 September 2026", 15, BOEING, bold=True).to_edge(DOWN, buff=0.55)
        xl = tx("aircraft built", 13, GREY_B).next_to(ax, DOWN, buff=0.45)
        src = source("The Boeing Company, Form 10-K 2025 (program accounting) and Form 10-Q, third quarter of 2026", size=12)
        beat(self,
             "If the early aircraft cost far more than their price, does every early delivery show a loss? Not at Boeing. "
             "<bookmark mark='a'/> Boeing uses program accounting. It estimates how many aircraft a programme will "
             "build, the accounting quantity, and what all of them will cost, and books each delivery at the programme's "
             f"average. <bookmark mark='b'/> In our model the average over fifteen hundred aircraft is {avg:.0f} million "
             "dollars. <bookmark mark='c'/> The early aircraft cost more than that, and the excess is not counted as a "
             "loss: it is carried on the balance sheet as deferred production costs, <bookmark mark='d'/> to be paid back "
             "by the cheaper aircraft built later. <bookmark mark='e'/> Boeing's 777X, not yet delivered, already carried "
             f"{A['dpc'] / 1e3:.1f} billion dollars of them in September 2026. The method is honest only if the estimates "
             "of quantity and cost are right.",
             base=[pa, xl, src], steps=[curve, line, [red, lr], [green, lg], dpc])

    def quantities(self):
        A = R["accounting"]
        names = {"737": "737", "787": "787", "777": "777", "777x": "777X"}
        rows = VGroup()
        top_v = 13000
        L = 8.0
        for i, k in enumerate(("737", "787", "777", "777x")):
            y = 1.7 - 1.05 * i
            aq, cum, und = A["aq"][k], A["cum"][k], A["undel"][k]
            frame = Rectangle(width=L * aq / top_v, height=0.42, stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0)
            frame.move_to([-3.6 + L * aq / top_v / 2, y, 0])
            d = Rectangle(width=max(L * cum / top_v, 0.02), height=0.42, stroke_width=0, fill_color=BOEING, fill_opacity=0.95)
            d.move_to([-3.6 + L * cum / top_v / 2, y, 0])
            d.grow = LEFT
            o = Rectangle(width=max(L * und / top_v, 0.02), height=0.42, stroke_width=0, fill_color=PRICE, fill_opacity=0.6)
            o.move_to([-3.6 + L * (cum + und / 2) / top_v, y, 0])
            o.grow = LEFT
            nm = tx(names[k], 18, WHITE, bold=True).move_to([-4.0, y, 0], aligned_edge=RIGHT)
            lab = tx(f"{cum:,} delivered + {und:,} on firm order; accounting quantity {aq:,}", 13, GREY_A).next_to(frame, DOWN, buff=0.06).align_to(frame, LEFT)
            rows.add(VGroup(nm, frame, d, o, lab))
        key = VGroup(tx("delivered", 14, BOEING, bold=True), tx("firm orders", 14, PRICE, bold=True),
                     tx("outline: the accounting quantity", 14, GREY_B)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.75)
        src = source("The Boeing Company, Form 10-K 2025 and Form 10-Q, third quarter of 2026: accounting quantities, "
                     "deliveries and firm orders at 31 December 2025", size=12)
        beat(self,
             "Here are Boeing's accounting quantities at the end of 2025, set against what it had delivered and what "
             f"was on firm order. <bookmark mark='a'/> For the 737, {A['aq']['737']:,} aircraft, fewer than the "
             f"{A['cum']['737'] + A['undel']['737']:,} already delivered or ordered: Boeing counts only the production it "
             "can estimate reliably. <bookmark mark='b'/> The 787 is the same. <bookmark mark='c'/> The original 777 is "
             f"almost finished. <bookmark mark='d'/> The 777X is different: an accounting quantity of {A['aq']['777x']}, "
             f"against {A['undel']['777x']} orders and no deliveries. Boeing raised it by a hundred and fifty in 2025, so its "
             f"estimate of the programme's margin counts on {A['aq']['777x'] - A['undel']['777x']} aircraft that nobody has "
             "ordered yet.",
             base=[key, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def reach(self):
        A = R["accounting"]
        pa = viz.plot_axes([2012, 2028], [0, 1], x_length=10.0, y_length=1.0, xticks=[2013, 2016, 2020, 2024, 2027],
                           xfmt=lambda v: f"{int(v)}", grid=False, size=14).move_to([0, 1.3, 0])
        ax = pa.ax
        launch = marker(ax, 2013, 0.5, "launched, 2013", BOEING, side=UP)
        target = marker(ax, A["x_target"], 0.5, f"first delivery promised: {A['x_target']}", PRICE, side=UP)
        now = marker(ax, A["x_first"], 0.5, f"now expected: {A['x_first']}", BAD, side=UP)
        arr = Arrow(ax.c2p(A["x_target"], 0.35), ax.c2p(A["x_first"], 0.35), buff=0.1, stroke_width=4, color=BAD)
        bars_ = vbars([("2024", A["rf777x"][2024], BAD, f"-${A['rf777x'][2024]:.1f}bn"),
                       ("2025", A["rf777x"][2025], BAD, f"-${A['rf777x'][2025]:.1f}bn")], base_y=-2.5, height=2.2, width=1.1,
                      gap=0.8, x0=1.6)
        bl = VGroup(tx("the 777X's reach-forward losses,", 16, BAD, bold=True),
                    tx("booked at once", 16, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([-2.4, -1.3, 0])
        src = source("The Boeing Company, Forms 10-K 2013 and 2025; Form 10-Q, third quarter of 2026", size=12)
        beat(self,
             "And when the estimates go wrong? If a programme's expected costs come to exceed its expected revenue, the "
             "whole expected loss over the accounting quantity is booked at once. This is a reach-forward loss. "
             "<bookmark mark='a'/> Boeing launched the 777X in 2013, <bookmark mark='b'/> promising its first delivery in "
             f"{A['x_target']}. <bookmark mark='c'/> In its latest report, first delivery is expected in {A['x_first']}, "
             "seven years late, after certification delays and an engine durability problem. <bookmark mark='d'/> The "
             f"delays added to costs, and Boeing booked reach-forward losses on the 777X of {A['rf777x'][2024]:.1f} billion "
             f"dollars in 2024 and {A['rf777x'][2025]:.1f} billion in 2025, all of it for aircraft not yet delivered.",
             base=[pa, src], steps=[launch, target, [now, arr], [bars_, bl]])

    def losses(self):
        A = R["accounting"]
        items = [("2023", A["bca"][2023] / 1e3, BAD, f"-${-A['bca'][2023] / 1e3:.1f}bn"),
                 ("2024", A["bca"][2024] / 1e3, BAD, f"-${-A['bca'][2024] / 1e3:.1f}bn"),
                 ("2025", A["bca"][2025] / 1e3, BAD, f"-${-A['bca'][2025] / 1e3:.1f}bn"),
                 ("2026, nine months", A["q9"] / 1e3, BAD, f"-${-A['q9'] / 1e3:.1f}bn")]
        rows = hbars(items, max_value=8.5, x0=-1.0, top=1.4, row=0.85, length=5.0, size=18, bar_h=0.5)
        src = source("The Boeing Company, Form 10-K 2025 and Form 10-Q, third quarter of 2026: Commercial Airplanes, loss from "
                     "operations", size=12)
        beat(self,
             "Put it together and here is Boeing's airliner business, the part that makes the jets. "
             f"<bookmark mark='a'/> It lost {-A['bca'][2023] / 1e3:.1f} billion dollars in 2023, "
             f"<bookmark mark='b'/> {-A['bca'][2024] / 1e3:.1f} billion in 2024, a year with a door plug, the FAA's cap "
             f"and a strike of {get('ba.strike.2024'):.0f} days that halted most airliner production, <bookmark mark='c'/> and {-A['bca'][2025] / 1e3:.1f} billion in 2025, most of that the 777X. "
             f"<bookmark mark='d'/> In the first nine months of 2026 the loss narrowed to {-A['q9'] / 1e3:.1f} billion, as "
             "deliveries rose. A business with ten years of orders lost money on its airliners in every period shown.",
             base=[rows.axis, head("Boeing Commercial Airplanes: loss from operations"), src],
             steps=[rows[0], rows[1], rows[2], rows[3]])
