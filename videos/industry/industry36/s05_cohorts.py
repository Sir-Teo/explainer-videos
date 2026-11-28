from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403

COH = ["#7EC8F5", "#9FE0D0", "#7BD88F", "#F6C453", "#F2A65A", "#FF8FB1", "#B58CFF", "#C9D3E0"]


class Cohorts(VoiceoverScene):
    def construct(self):
        card(self, 4, "The layer cake", "Why does a software company value customers it already has above all others?",
             "Chapter four. The layer cake. A subscription company's revenue is a stack of customers, piled up year by year. "
             "What happens to each layer decides everything.", lit=("moat",))
        self.cake()
        self.nrr()
        self.value()
        self.big()

    def _stack(self, m, nrr_label):
        years = m.shape[1]
        top = m.sum(axis=0).max()
        base_y, height, width, gap = -2.4, 4.4, 0.95, 0.35
        x0 = -(years * width + (years - 1) * gap) / 2 + width / 2 - 0.6
        layers = [VGroup() for _ in range(years)]
        for y in range(years):
            b = base_y
            for c in range(years):
                v = m[c, y]
                if v <= 0:
                    continue
                h = height * v / top
                layers[c].add(Rectangle(width=width, height=h, stroke_width=0.5, stroke_color="#0E1117", fill_color=COH[c % len(COH)],
                                        fill_opacity=0.95).move_to([x0 + y * (width + gap), b + h / 2, 0]))
                b += h
        xl = VGroup(*[tx(f"year {y + 1}", 13, GREY_B).move_to([x0 + y * (width + gap), base_y - 0.25, 0]) for y in range(years)])
        lab = tx(nrr_label, 16, GREY_A).to_edge(UP, buff=1.0)
        return layers, xl, lab

    def cake(self):
        Cc = R["cohorts"]
        import numpy as _np
        m = _np.array(Cc["matrix"])
        layers, xl, lab = self._stack(m, f"ARR by the year customers joined; each year's newcomers 25% more than the last, net retention {100 * Cc['nrr_works']:.0f}%")
        hd = tx("the layer cake", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        tag = estimate_tag("the Works: churn 8% and expansion 10% a year for every cohort", size=12)
        beat(self,
             "Draw a company's revenue by when each customer arrived. <bookmark mark='a'/> In year one, the first customers. "
             "<bookmark mark='b'/> In year two they are still there, a little bigger, and a new, larger layer arrives on top. "
             "<bookmark mark='c'/> Year after year the layers pile up. <bookmark mark='d'/> In the Works, the customers who "
             f"stay grow faster than the ones who leave shrink, so every layer is worth a little more each year: net retention "
             f"of {100 * Cc['nrr_works']:.0f} per cent. By year eight, most of the revenue comes from customers won years ago, "
             "who cost nothing more to win.",
             base=[hd, lab, xl, tag], steps=[layers[0], layers[1], VGroup(*layers[2:5]), VGroup(*layers[5:])])

    def nrr(self):
        Cc = R["cohorts"]
        items = [("Snowflake, January 2026", Cc["snow"], SUB, f"{Cc['snow']}%"), ("Datadog, December 2025", Cc["ddog"], SUB, f"about {Cc['ddog']}%"),
                 ("the Works' company", 100 * Cc["nrr_works"], GA, f"{100 * Cc['nrr_works']:.0f}%")]
        rows = hbars(items, max_value=130, x0=0.6, top=1.2, row=1.0, length=5.0, size=17, bar_h=0.55)
        hd = tx("net revenue retention: this year's revenue from last year's customers", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        line100 = DashedLine(rows.axis.get_bottom() + RIGHT * 5.0 * 100 / 130 + UP * 0.1, rows.axis.get_top() + RIGHT * 5.0 * 100 / 130,
                             color=GREY_B, stroke_width=1.5)
        note = tx("above 100%: the old customers alone make the company grow", 17, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Snowflake, Form 10-K for fiscal 2026; Datadog, Form 10-K for 2025", size=12)
        beat(self,
             "The industry has a name for the thickness of each layer: net revenue retention, this year's spending by last "
             f"year's customers. <bookmark mark='a'/> Snowflake's was {Cc['snow']} per cent at the start of 2026, "
             f"<bookmark mark='b'/> Datadog's about {Cc['ddog']}. These companies charge by use: as a customer stores more data "
             "or watches more servers, the bill rises without a new sale. <bookmark mark='c'/> The Works' company is at "
             f"{100 * Cc['nrr_works']:.0f}. <bookmark mark='d'/> Above a hundred, the company would grow even if it never won "
             "another customer.",
             base=[rows.axis, hd, line100, src], steps=[rows[0], rows[1], rows[2], note])

    def value(self):
        U = R["run"]
        L = U["ltv"]
        items = [("cost of winning $1 of new ARR", U["cac"], SALES, f"${U['cac']:.2f}"),
                 ("gross profit from it in year one", L[1], PROFIT, f"${L[1]:.2f}"),
                 ("over three years", L[3], PROFIT, f"${L[3]:.2f}"),
                 ("over ten years", L[10], PROFIT, f"${L[10]:.2f}")]
        rows = hbars(items, max_value=6.5, x0=0.8, top=1.6, row=0.9, length=5.0, size=17, bar_h=0.5)
        hd = tx("the Works: a dollar of new subscriptions, discounted at 10% a year", 20, WHITE, bold=True).to_edge(UP, buff=0.7)
        tag = estimate_tag("the Works: sales and marketing over new ARR; gross margin 78%; net retention 102%", size=12)
        beat(self,
             "Put a price on a layer. <bookmark mark='a'/> In the Works, winning one dollar of new subscriptions costs "
             f"{U['cac']:.2f} dollars of selling. <bookmark mark='b'/> In its first year that dollar brings in "
             f"{L[1]:.2f} of gross profit: a loss. <bookmark mark='c'/> Over three years, {L[3]:.2f}, counting money later as "
             f"worth less. <bookmark mark='d'/> Over ten, {L[10]:.2f}: {L[10] / U['cac']:.1f} times what it cost to win. The industry "
             "calls this the lifetime value against the cost of acquisition, and it is the whole argument for spending so "
             "much on selling.",
             base=[rows.axis, hd, tag], steps=list(rows))

    def big(self):
        Cc = R["cohorts"]
        c = stat_cards([(f"{Cc['now_big']}", "ServiceNow customers paying over $5m a year, end of 2025 (420 two years before)", SUB),
                        (f"{Cc['snow_big']}", "Snowflake customers paying over $1m a year, January 2026 (576 a year before)", PROFIT)],
                       y=1.6, size=44, span=12)
        few = VGroup(*[draw.person(0.45, color=SUB) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to([-3.6, -1.4, 0])
        many = draw.crowd(40, 0.4, color=PROFIT, cols=10).move_to([2.6, -1.4, 0])
        arr = Arrow(few.get_right(), many.get_left(), buff=0.3, color=GREY_B, stroke_width=3)
        src = source("ServiceNow, Form 10-K for 2025; Snowflake, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "So the prize is the big customer who keeps growing. <bookmark mark='a'/> ServiceNow had "
             f"{Cc['now_big']} customers paying it more than five million dollars a year at the end of 2025, up from 420 two "
             f"years earlier. <bookmark mark='b'/> Snowflake had {Cc['snow_big']} paying more than a million, up from 576 in a "
             "year. In this series' reading, that is where the sales effort goes: turning a small first contract, often "
             "one team's, into the whole company's.",
             base=[src, few, arr, many], steps=[c[0], c[1]])
