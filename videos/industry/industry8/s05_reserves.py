from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403


class Reserves(VoiceoverScene):
    def construct(self):
        card(self, 4, "Reserves are an economic number", "Can oil in the ground disappear without anyone pumping it?",
             "Chapter four. Reserves are an economic number.", lit=("unit", "change"))
        self.nested()
        self.exxon()

    def nested(self):
        boxes = VGroup()
        specs = [("oil in place: all of it, wherever it is", 6.4, 4.4, "#3A3226"),
                 ("technically recoverable: could be produced with today's methods", 5.2, 3.3, "#5C4E3A"),
                 ("proved reserves: worth producing at today's prices and costs", 3.6, 2.0, CRUDE)]
        for k, (lab, w, h, col) in enumerate(specs):
            b = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=WHITE if k == 2 else GREY_C,
                                 stroke_width=2, fill_color=col, fill_opacity=0.9)
            b.move_to([-2.4, -0.6 - (4.4 - h) / 2 + 0.0, 0]).align_to([-2.4, -2.8, 0], DOWN)
            t = tx(lab, 15, WHITE).next_to(b.get_top(), DOWN, buff=0.15)
            if t.width > w - 0.3:
                t.scale_to_fit_width(w - 0.3)
            boxes.add(VGroup(b, t))
        hub = VGroup(tx("Hubbert, 1956:", 17, GREY_B), tx("'only about a third of the oil underground", 17, WHITE),
                     tx("is being recovered'", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.8, 1.3, 0])
        rule = VGroup(tx("The SEC's rule for listed companies:", 17, GREY_B),
                      tx("value the oil at the average price", 17, WHITE),
                      tx("of the last twelve months", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [3.8, -1.0, 0])
        src = source("Hubbert (1956); ExxonMobil, Form 10-K for 2020 (the SEC's pricing rule)", size=13)
        with self.voiceover(
            "How much oil does a company have? There are three answers, nested inside each other. "
            "<bookmark mark='a'/> All the oil in the rock, wherever it is: most of it will never come out. "
            "<bookmark mark='b'/> The part that could come out with today's methods. In 1956 the geologist King "
            "Hubbert reckoned only about a third of the oil underground was being recovered; better methods keep "
            "raising that share. <bookmark mark='c'/> And the part worth producing at today's prices and costs: proved "
            "reserves, the number a company reports. <bookmark mark='d'/> For companies listed in America, the "
            "Securities and Exchange Commission sets the price to use: the average of the last twelve months. So a "
            "company's reserves can shrink, or grow, without a single barrel moving."
        ) as vo:
            self.play(FadeIn(src))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(boxes[k], scale=0.95), run_time=1.0)
                if k == 1:
                    self.play(FadeIn(hub, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(rule, shift=LEFT * 0.2), Indicate(boxes[2], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def exxon(self):
        r19, r20, r21, r25 = (get(f"xom.reserves.{y}") for y in (2019, 2020, 2021, 2025))
        kearl = get("xom.kearl")
        unit = 0.1  # bn boe per dot
        n = int(round(r19 / unit))
        cols = 16
        dots = VGroup(*[Square(0.2, stroke_width=0, fill_color=CRUDE, fill_opacity=1) for _ in range(n)]).arrange_in_grid(
            cols=cols, buff=0.07)
        dots.move_to([-3.2, -0.5, 0])
        lost = int(round((r19 - r20) / unit))
        back = int(round((r21 - r20) / unit))
        k_kearl = int(round(kearl / unit))
        order = list(range(n - 1, -1, -1))  # lose from the end of the grid
        kearl_idx = order[:k_kearl]
        other_idx = order[k_kearl:lost]
        year = ValueTracker(2019)
        yl = draw.memo_redraw(lambda: int(round(year.get_value())), lambda y: tx(f"end of {y}", 26, PRICE, bold=True),
                              lambda m: m.next_to(dots, UP, buff=0.3))
        num = {2019: r19, 2020: r20, 2021: r21, 2025: r25}
        vl = draw.memo_redraw(lambda: int(round(year.get_value())),
                              lambda y: tx(f"{num.get(y, r25):.1f} billion barrels of oil equivalent, proved", 20, WHITE),
                              lambda m: m.next_to(dots, DOWN, buff=0.3))
        wti = R["long"]
        ann = dict(zip(wti["years"], wti["real_annual"]))
        pe = _fe_nominal()
        prices = VGroup(*[tx(f"{y}: WTI averaged ${pe[y]:.0f}", 18, GREY_A) for y in (2019, 2020, 2021)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, 1.6, 0])
        kl = VGroup(tx(f"{kearl:.1f}bn barrels of tar at Kearl,", 17, STATE), tx("Canada's oil sands", 17, STATE)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([3.9, -0.4, 0])
        ol = tx("and more in Canada and the US", 17, GREY_B).next_to(kl, DOWN, buff=0.15).align_to(kl, LEFT)
        loss = tx(f"{r19 - r20:.1f}bn barrels gone from the books,", 18, WHITE).next_to(ol, DOWN, buff=0.35).align_to(kl, LEFT)
        loss2 = tx("none of it produced", 18, WHITE, bold=True).next_to(loss, DOWN, buff=0.05).align_to(kl, LEFT)
        src = source("Exxon Mobil Corporation, Forms 10-K for 2019, 2020, 2021 and 2025; WTI (EIA via FRED)", size=13)
        del ann
        with self.voiceover(
            "Here is what that means for the biggest American oil company. <bookmark mark='a'/> At the end of 2019 "
            f"ExxonMobil reported {r19:.1f} billion barrels of oil and gas, as oil equivalent, in proved reserves. Each "
            "square is a hundred million barrels. <bookmark mark='b'/> Then 2020: oil prices collapsed, and the "
            "twelve-month average fell with them. <bookmark mark='c'/> At that price, "
            f"{kearl:.1f} billion barrels of tar at Kearl, in Canada's oil sands, no longer paid, and so no longer "
            "counted. More went in Canada and the United States, and cuts to drilling plans took more. "
            f"<bookmark mark='d'/> Proved reserves fell to {r20:.1f} billion barrels. Nothing had been pumped, and "
            "nothing had leaked. The oil was exactly where it had been. <bookmark mark='e'/> A year later, prices "
            f"recovered and reserves were back to {r21:.1f}; at the end of 2025, {r25:.1f}. Reserves are not a "
            "quantity of rock. They are a forecast, at a price."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.add(yl, vl)
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(prices[:2]))
            vo.wait_until("c")
            self.play(*[dots[i].animate.set_fill(STATE) for i in kearl_idx], FadeIn(kl))
            self.play(*[dots[i].animate.set_fill("#E8A04E") for i in other_idx], FadeIn(ol))
            vo.wait_until("d")
            year.set_value(2020)
            self.play(*[dots[i].animate.set_fill("#2A2F38", 1) for i in kearl_idx + other_idx], FadeIn(loss), FadeIn(loss2),
                      run_time=1.6)
            vo.wait_until("e")
            year.set_value(2021)
            self.play(FadeIn(prices[2]), *[dots[i].animate.set_fill(CRUDE, 1) for i in (kearl_idx + other_idx)[::-1][:back]])
            year.set_value(2025)
            extra = int(round((r25 - r21) / unit))
            self.play(*[dots[i].animate.set_fill(CRUDE, 1) for i in (kearl_idx + other_idx)[::-1][back:back + extra]])
        for m in (yl, vl):
            m.clear_updaters()
        self.clear_scene()


def _fe_nominal() -> dict:
    """WTI's yearly average in dollars of the day (EIA spot, monthly), for the three years shown."""
    from explainer.industry.data.fetch import read
    rows = [r for r in read("eia_petroleum") if r["series"] == "RWTC"]
    out = {}
    for y in (2019, 2020, 2021):
        v = [r["value"] for r in rows if str(r["period"]).startswith(str(y))]
        out[y] = sum(v) / len(v)
    return out
