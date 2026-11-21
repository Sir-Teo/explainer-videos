from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403

YEAR_COL = {2023: GREY_B, 2024: CTRL, 2025: TOLL, 2026: ROW}


class Estimates(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The estimates, \ and what they cannot say", r"How much did the charge move traffic and "
             r"buses, \ and how sure can we be?", "Chapter five. The estimates, and what they cannot say.",
             scale=("city",), horizon=("a year",))
        self.crossings()
        self.buses()
        self.official()

    def crossings(self):
        D = load("did")
        rows = [r for r in D["rows"] if r["year"] in (2023, 2024, 2025, 2026)]
        ax = plane([0, len(rows) + 1], [-6, 4], center=LEFT * 0.9 + DOWN * 0.2, x_length=10.4, y_length=4.6,
                   xticks=[], yticks=[-6, -4, -2, 0, 2, 4],
                   ylabel=r"tunnels minus other crossings, \ year-on-year change, \ \%",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        zero = seg(ax, 0, 0, len(rows) + 1, 0, GREY_C, 1.4)
        b = VGroup()
        for k, r in enumerate(rows):
            v = 100 * r["did"]
            p0, p1 = ax.ax.c2p(k + 0.6, 0), ax.ax.c2p(k + 1.4, v)
            b.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                            fill_color=YEAR_COL[r["year"]], fill_opacity=0.85).move_to((p0 + p1) / 2))
        yl = VGroup()
        for y in (2023, 2024, 2025, 2026):
            ks = [k for k, r in enumerate(rows) if r["year"] == y]
            if ks:
                yl.add(label(str(y) + (r" \ (placebo)" if y < 2025 else ""), font_size=15,
                             color=YEAR_COL[y]).next_to(ax.ax.c2p((ks[0] + ks[-1]) / 2 + 1, -6), DOWN, buff=0.12))
        mean25 = seg(ax, min(k for k, r in enumerate(rows) if r["year"] == 2025) + 0.5, 100 * D["effect"],
                     max(k for k, r in enumerate(rows) if r["year"] == 2025) + 1.5, 100 * D["effect"], WHITE, 2.4)
        plc = seg(ax, 0.5, 100 * D["placebo_mean"], min(k for k, r in enumerate(rows) if r["year"] == 2025) + 0.5,
                  100 * D["placebo_mean"], WHITE, 2.0, dashed=True)
        side = VGroup(
            label(rf"2025: \ {100 * D['effect']:.1f}\%".replace("-", "{-}"), font_size=19, color=TOLL),
            label(rf"placebo years: \ {100 * D['placebo_mean']:.1f}\%".replace("-", "{-}"), font_size=19,
                  color=CTRL),
            label(rf"net of the drift: \ {100 * D['adjusted']:.1f}\% \ (s.e.\ {100 * D['se_adjusted']:.1f})".replace(
                "-", "{-}"), font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.4)
        tag = data_tag(r"MTA crossings; \ agora.congestion.yoy\_did", corner=DL, font_size=12)
        with self.voiceover(
            "The crossings first. <bookmark mark='a'/> Each bar is one month: the tunnels' year-on-year change minus "
            "the other crossings', in percent. The grey and blue bars are 2023 and 2024, before any charge: the "
            "placebos. <bookmark mark='b'/> They are not zero. The tunnels were losing ground by "
            f"{say_pct(-D['placebo_mean'], 1)} a year before anything happened. <bookmark mark='c'/> In 2025, the red "
            f"bars, the gap averages {say_pct(-D['effect'], 1)}. <bookmark mark='d'/> Net of the drift, the charge's "
            f"effect on the tunnels is about {say_pct(-D['adjusted'], 1)}, with a standard error of "
            f"{say_pct(D['se_adjusted'], 1)}: small, and only just distinguishable from zero. The orange bars of 2026 "
            "compare two charged years, and look like the drift again."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, UP if r["did"] < 0 else DOWN) for x, r in zip(b, rows)
                                    if r["year"] < 2025], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(plc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(x, UP if r["did"] < 0 else DOWN) for x, r in zip(b, rows)
                                    if r["year"] == 2025], lag_ratio=0.05), Create(mean25), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]), LaggedStart(*[GrowFromEdge(x, UP if r["did"] < 0 else DOWN)
                                                     for x, r in zip(b, rows) if r["year"] == 2026],
                                                   lag_ratio=0.05), run_time=2.0)
        self.clear_scene()

    def buses(self):
        Bu, V = load("buses"), load("vmt")
        cards = point_cards([
            (r"buses in the district", rf"weekday peak speed {Bu['cbd_2024']:.2f} mph in 2024, \ "
             rf"{Bu['cbd_2025']:.2f} in 2025: \ {100 * Bu['cbd_change']:.1f}\% faster",
             BUS),
            (r"against buses outside", rf"{100 * Bu['effect']:+.1f}\% \ (placebo year 2024: "
             rf"{100 * Bu['placebo']:+.1f}\%)".replace("-", "{-}"), CTRL),
            (r"miles driven in the zone", rf"{100 * V['crz_change']:+.1f}\% in 2025, \ on its free highways "
             rf"{100 * V['er_change']:+.1f}\%".replace("-", "{-}"), TOLL),
            (r"what it adds up to", r"fewer miles, \ slightly faster buses, \ a small effect on the tolled tunnels: "
             r"\ a modest, \ measurable change", DATA),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"buses and miles", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = data_tag(r"MTA bus speeds and vehicle-miles in the business district", corner=DL, font_size=12)
        with self.voiceover(
            "Then buses and miles. <bookmark mark='a'/> At the weekday peak, buses inside the business district "
            f"averaged {Bu['cbd_2024']:.2f} miles an hour in 2024 and {Bu['cbd_2025']:.2f} in 2025. <bookmark "
            f"mark='b'/> Against buses outside, the gain is {say_pct(Bu['effect'], 1)}, where the placebo year "
            f"shows {say_pct(Bu['placebo'], 1)}. <bookmark mark='c'/> Miles driven in the zone fell "
            f"{say_pct(-V['crz_change'], 1)}, and on its two free highways {say_pct(-V['er_change'], 1)}. <bookmark "
            "mark='d'/> Fewer miles, slightly faster buses, a small effect on the tolled tunnels: a modest, "
            "measurable change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def official(self):
        O, V = load("official"), load("vmt")
        cards = point_cards([
            (r"the state's figure", rf"{O['fewer_share'] * 100:.0f}\% fewer vehicles entering, \ against a "
             r"projection of what entries would have been", TOLL),
            (r"this study's", rf"{100 * V['crz_change']:.1f}\% fewer miles in the zone than a year before; \ "
             r"small effects against comparison crossings and routes".replace("-", "{-}"), CTRL),
            (r"why they differ", r"entries are not miles; \ a projection is not a comparison group; \ the free "
             r"bridges are not in the data", DATA),
            (r"what the design cannot say", r"how many trips were given up rather than moved, \ who paid, \ or "
             r"what happens when the toll rises", MODEL),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"two answers, \ and why", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Office of the Governor (5 January 2026); \ this film", corner=DL, font_size=12)
        with self.voiceover(
            "So which is it? <bookmark mark='a'/> The state reported eleven percent fewer vehicles entering the "
            "zone, against a projection of what entries would have been without the charge. <bookmark mark='b'/> "
            f"This study finds {say_pct(-V['crz_change'], 1)} fewer miles driven in the zone than a year before, and "
            "small effects against comparison crossings and routes. <bookmark mark='c'/> They need not conflict. "
            "Entries are not miles; a projection is a model of the counterfactual, a comparison group is another; "
            "and the free bridges are in neither. <bookmark mark='d'/> And no design here can say how many trips "
            "were given up rather than moved, who paid, or what a higher toll would do. That takes a model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
