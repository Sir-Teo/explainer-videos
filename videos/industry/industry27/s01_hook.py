from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.pair()
        self.years()
        self.suez()
        self.title()

    def pair(self):
        H = R["hook"]
        box = draw.shoebox(1.2).move_to([-5.0, 0.6, 0])
        cont = draw.container(3.4, color=BOX).move_to([-0.6, 0.6, 0])
        vessel = draw.ship(3.6).move_to([4.4, 0.6, 0])
        a1 = Arrow([-4.2, 0.6, 0], [-2.5, 0.6, 0], buff=0, stroke_color=GREY_B, stroke_width=3)
        a2 = Arrow([1.3, 0.6, 0], [2.5, 0.6, 0], buff=0, stroke_color=GREY_B, stroke_width=3)
        l1 = tx(f"about {H['pairs']:,.0f} pairs fill a 40-foot box", 17, BOX).next_to(cont, DOWN, buff=0.3)
        l2 = tx(f"ZIM's average 2025 freight: ${H['rate'][2025]:,.0f} per 20-foot unit", 17, RATE).next_to(vessel, DOWN, buff=0.3)
        res = tx(f"about {100 * H['per_pair'][2025]:.0f} cents a pair, Asia to the world", 30, GOOD, bold=True).move_to([0, -2.0, 0])
        tag = estimate_tag(f"this series' arithmetic; the pairs a box holds are this series' assumption ({H['pairs_span'][0]:,.0f}-{H['pairs_span'][1]:,.0f})", size=12)
        src = source("ZIM Integrated Shipping Services, Form 20-F for 2025: average freight rate per TEU carried", size=12)
        beat(self,
             "A pair of trainers is made in Vietnam and sold in Ohio. <bookmark mark='a'/> In its box it goes into a forty "
             f"foot steel container with, at a rough count, about {H['pairs']:,.0f} other pairs. <bookmark mark='b'/> In 2025 "
             f"the container line ZIM was paid, on average, {H['rate'][2025]:,.0f} dollars to carry each twenty-foot unit "
             "of cargo, about half a forty-foot box, across the sea. <bookmark mark='c'/> So the ocean voyage, ten thousand "
             f"miles or more, cost the pair of trainers about {100 * H['per_pair'][2025]:.0f} cents.",
             base=[tag, src], steps=[[box, a1, cont], [l1, a2, vessel, l2], res])

    def years(self):
        H = R["hook"]
        items = [(str(y), 100 * H["per_pair"][y], BAD if H["per_pair"][y] > 1 else GOOD, f"{100 * H['per_pair'][y]:.0f}c")
                 for y in range(2016, 2026)]
        cols = vbars(items, base_y=-2.0, height=3.6, width=0.7, gap=0.4, size=14, max_value=140)
        lab = tx("the ocean freight on one pair of trainers, at ZIM's average rate each year", 17, GREY_A).to_edge(UP, buff=0.8)
        tag = estimate_tag("this series' arithmetic, at 5,000 pairs a 40-foot box", size=12)
        src = source("ZIM Integrated Shipping Services, Forms 20-F for 2020, 2021, 2023 and 2025", size=12)
        beat(self,
             "And the same pair, year by year. <bookmark mark='a'/> From 2016 to 2019, about forty cents. "
             f"<bookmark mark='b'/> In 2021, {100 * H['per_pair'][2021]:.0f} cents, and in 2022 "
             f"{100 * H['per_pair'][2022]:.0f}: the freight tripled in two years. <bookmark mark='c'/> In 2023 it fell back "
             f"to {100 * H['per_pair'][2023]:.0f}. Moving goods across an ocean has become nearly free, and the price of "
             "nearly free can still triple in a year.",
             base=[lab, tag, src], steps=[VGroup(*cols[:4]), VGroup(*cols[4:7]), VGroup(*cols[7:])])

    def suez(self):
        H = R["hook"]
        s = H["suez"]
        pts = {i: v for i, (d, v) in enumerate(sorted(s.items()))}
        days = sorted(s)
        ticks = [i for i, d in enumerate(days) if d[8:] in ("10", "20", "25", "31") or d.endswith("04-10")]
        ch = line_chart({"ships through the Suez Canal a day": (pts, SEA)}, x=(0, len(days) - 1), y=(0, 80),
                        xticks=ticks, yticks=[0, 20, 40, 60, 80], xfmt=lambda v: days[int(round(v))][5:].replace("-", "/"),
                        ylabel="ships passing through the Suez Canal each day, March and April 2021", width=9.4, height=4.2,
                        center=(-0.8, -0.45), label_end=False)
        lo = days.index(H["low_day"])
        m1 = marker(ch.ax, lo, H["low"], f"{H['low_day'][8:]} March: {H['low']:.0f} ships", BAD, side=RIGHT)
        vessel = draw.ship(2.0).move_to([5.4, 1.8, 0]).rotate(0.35)
        src = source("IMF PortWatch, daily chokepoint transits (estimates from ship positions); E2open, Form 10-K of May 2021", size=12)
        beat(self,
             "Yet the whole system runs through a few narrow places. <bookmark mark='a'/> In March 2021 about "
             f"{H['before']:.0f} ships a day passed through the Suez Canal. <bookmark mark='b'/> Then a container ship, the "
             f"Ever Given, ran aground across it, and for {H['days']:.0f} days almost nothing moved: on {H['low_day'][8:]} "
             f"March, {H['low']:.0f} ships. The route between Asia and Europe, shut by one ship lying sideways in a "
             "canal.",
             base=[ch.frame, vessel, src], steps=[ch.lines["ships through the Suez Canal a day"], m1])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-seven: shipping and ports. How did moving a tonne across an ocean "
                            "become nearly free, and why do the companies that do it swing between fortune and ruin?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
