from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

PICK = ["Health care and social assistance", "Professional and technical services", "Construction",
        "Hotels and restaurants", "Manufacturing", "Retail trade", "Finance and insurance", "Wholesale trade",
        "Information", "Mining", "Utilities", "Real estate"]


class Split(VoiceoverScene):
    def construct(self):
        card(self, 7, "Who gets the value added", "Of what each industry adds, how much goes to workers?",
             "Chapter seven. Who gets the value added.", lit=("dollar",))
        V = {d["sector"]: d for d in R["va"]}
        allv = R["va"][0]
        L = 7.6
        rows = VGroup()
        for name in ["All industries (GDP)"] + PICK:
            d = allv if name == "All industries (GDP)" else V[name]
            parts = [(d["comp"], I.PROFIT), (d["tax"], I.TAX), (d["gos"], I.MONEY)]
            bars = VGroup(*[Rectangle(width=max(L * max(p, 0) / 100, 0.01), height=0.32, fill_color=c,
                                      fill_opacity=0.9, stroke_width=0) for p, c in parts]).arrange(RIGHT, buff=0)
            lab = T(short(name) if name != "All industries (GDP)" else "Whole economy", 19,
                    I.ACCENT if name == "All industries (GDP)" else I.TEXT)
            w = T(f"{d['comp']:.0f}%", 15, "#0E1117").move_to(bars[0])
            rows.add(VGroup(lab, bars, w))
        for i, r in enumerate(rows):
            y = 2.55 - 0.42 * i - (0.15 if i else 0)
            r[0].move_to(np.array([-2.6, y, 0]), aligned_edge=RIGHT)
            r[1].move_to(np.array([-2.35, y, 0]), aligned_edge=LEFT)
            r[2].move_to(r[1][0])
        legend = VGroup(*[VGroup(Square(0.2, fill_color=c, fill_opacity=1, stroke_width=0), T(t, 17, I.TEXT)).arrange(
            RIGHT, buff=0.1) for t, c in (("wages and benefits", I.PROFIT), ("taxes on production", I.TAX),
                                          ("operating surplus: profit, interest, rent, depreciation", I.MONEY))]
                        ).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.75)
        src = source("BEA, GDP by Industry, components of value added (TVA112), 2025", corner=DR)
        with self.voiceover(
            "Value added is paid out to someone. <bookmark mark='a'/> Across the whole economy, about half goes to "
            "workers as wages and benefits, about seven percent to taxes on production, and the rest, about 42 "
            "percent, is the operating surplus: profit, interest, rent and the wear on machines and buildings. "
            "<bookmark mark='b'/> Industry by industry, the split is very different. In health care, 81 cents of "
            "every dollar of value added goes to the people who work there; in professional services, 68; in "
            "construction and in restaurants, more than 60. <bookmark mark='c'/> In manufacturing it is close to half "
            "and half. <bookmark mark='d'/> In information, mining and utilities, about 60 cents goes to the owners "
            "of the equipment, the pipes, the networks and the software. <bookmark mark='e'/> And in real estate "
            "almost all of it does, 85 cents, because the value added of a building is mostly its rent. Who gets "
            "the money in an industry depends on whether its product is made by people or by things."
        ) as vo:
            for item, g_ in zip(legend, (draw.person(0.3, color=I.PROFIT), draw.coin(0.12, color=I.TAX),
                                         draw.factory(0.45, color=I.MONEY))):
                g_.next_to(item, LEFT, buff=0.1)
                item.add(g_)
            legend.arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.75)
            if legend.width > 13.0:
                legend.scale_to_fit_width(13.0)
            big = draw.coin(0.32).move_to([-6.3, 2.55, 0])
            self.play(FadeIn(legend), FadeIn(src), FadeIn(big, scale=1.4))
            vo.wait_until("a")
            flows = [draw.coin_flow(big.get_center(), seg.get_center(), n=n, r=0.1, arc=-0.5, run_time=1.3)
                     for seg, n in zip(rows[0][1], (5, 1, 4))]
            self.add(*[c for c, _ in flows])
            self.play(*[a_ for _, a_ in flows], FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT),
                      FadeOut(big, scale=0.4), run_time=1.6)
            self.remove(*[c for c, _ in flows])
            self.play(FadeIn(rows[0][2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in rows[1:5]], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in rows[5:9]], lag_ratio=0.3), run_time=2)
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in rows[9:12]], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(rows[12][0]), GrowFromEdge(rows[12][1], LEFT), FadeIn(rows[12][2]))
        self.clear_scene()
