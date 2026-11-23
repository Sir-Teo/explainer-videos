from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

FLAGLESS = {"Korea, Rep.": "South Korea", "Viet Nam": "Vietnam"}


class World(VoiceoverScene):
    def construct(self):
        card(self, 15, "Around the world", "Does every country's economy look like America's?",
             "Chapter fifteen. Around the world.", lit=("change",))
        self.shares()
        self.services()
        self.mfg()

    def shares(self):
        W = R["world"]
        items = [(FLAGLESS.get(c, c) + (f" ({y})" if y != 2025 else ""), m, "#F2A65A" if c != "United States" else
                  I.ACCENT, f"farms {a:.0f}%" if a is not None else "") for c, y, m, a in W]
        rows = viz.margin_ladder(items, max_value=30, bar_len=6.4, row_h=0.4, size=18, name_w=4.0,
                                 fmt=lambda v: f"{v:.0f}%")
        rows.move_to(RIGHT * 0.6 + DOWN * 0.3)
        head = T("Manufacturing as a share of GDP, 2025", 24, I.TEXT).to_edge(UP, buff=0.4)
        src = source("World Bank, World Development Indicators; the United States from BEA", corner=DR)
        with self.voiceover(
            "Other economies are built differently. <bookmark mark='a'/> In South Korea, China and Vietnam, "
            "manufacturing is about a quarter of GDP; in Mexico, Indonesia, Japan and Germany, around a fifth. "
            "<bookmark mark='b'/> In the United States, France and Britain it is under a tenth. <bookmark mark='c'/> "
            "Farming tells a story of income: it is about a quarter of Nigeria's economy and a sixth of India's, "
            "but around one percent in the rich countries, where a few farmers with large machines feed everyone "
            "else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.04), *[FadeIn(r[1]) for r in rows])
            vo.wait_until("a")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[:7]], run_time=1.6)
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[7:]], run_time=1.6)
            vo.wait_until("c")
            self.play(*[Indicate(r[3], color=I.ACCENT, scale_factor=1.1) for r in rows])
        self.clear_scene()

    def services(self):
        W = R["world_services"]
        items = [(FLAGLESS.get(c, c) + (f" ({y})" if y != 2025 else ""), v, "#4FD1C5", "") for c, y, v in W]
        rows = viz.margin_ladder(items, max_value=80, bar_len=6.4, row_h=0.4, size=18, name_w=4.0,
                                 fmt=lambda v: f"{v:.0f}%")
        rows.move_to(RIGHT * 0.6 + DOWN * 0.3)
        head = T("Services as a share of GDP, 2025", 24, I.TEXT).to_edge(UP, buff=0.4)
        src = source("World Bank, World Development Indicators (value added at basic prices)", corner=DR)
        by = {FLAGLESS.get(c, c): v for c, _, v in W}
        with self.voiceover(
            "And services, from shops and banks to hospitals and schools, are the largest part of every economy "
            f"here. <bookmark mark='a'/> About seven tenths of Britain's, France's and Japan's. <bookmark mark='b'/> "
            f"About three fifths of China's, Mexico's and Brazil's. <bookmark mark='c'/> And less than half of "
            "India's, Indonesia's and Vietnam's. As countries grow richer, the share of services rises: the same "
            "shift America went through, two chapters ago."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.04), *[FadeIn(r[1]) for r in rows])
            vo.wait_until("a")
            n = sum(1 for _, _, v in W if v > 65)
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[:n]], run_time=1.2)
            vo.wait_until("b")
            m = sum(1 for _, _, v in W if v > 50)
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[n:m]], run_time=1.2)
            vo.wait_until("c")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[m:]], run_time=1.2)
        self.clear_scene()
        assert by["United Kingdom"] > 70 and by["India"] < 50

    def mfg(self):
        S = R["world_mfg"]["share"]
        order = sorted(S.items(), key=lambda t: -t[1])
        rest = 100 - sum(v for _, v in order)
        items = [(FLAGLESS.get(c, c), v, "#E9655D" if c == "China" else ("#5DA9E9" if c == "United States" else
                                                                         "#8B95A7"), f"{v:.0f}%") for c, v in order]
        items.append(("Rest of the world", rest, "#3A4150", f"{rest:.0f}%"))
        tm = viz.treemap(items, 11.0, 5.2, 22).move_to(DOWN * 0.35)
        head = VGroup(TB(f"${R['world_mfg']['world']:.1f} trillion", 28, I.MONEY),
                      T("of manufacturing value added in the world, 2025", 22, I.TEXT)).arrange(RIGHT, buff=0.2
                                                                                               ).to_edge(UP, buff=0.4)
        src = source("World Bank (NV.IND.MANF.CD); the United States from BEA, 2025; latest year for each country",
                     corner=DR, size=14)
        with self.voiceover(
            "Now count manufacturing in dollars instead of shares. <bookmark mark='a'/> The world's factories added "
            "about 17.6 trillion dollars of value in 2025. <bookmark mark='b'/> China added more than a quarter of "
            "it, 27 percent. The United States, with a smaller share of its own economy in manufacturing but a much "
            "bigger economy, added about a sixth. <bookmark mark='c'/> Germany and Japan about five percent each. "
            "Part 61 of this series takes one industry, steel, through five of these countries to see why the same "
            "industry looks so different in each."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(tm[0], scale=0.95), FadeIn(tm[1], scale=0.95))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, scale=0.95) for b in tm[2:]], lag_ratio=0.15), run_time=1.6)
        self.clear_scene()
