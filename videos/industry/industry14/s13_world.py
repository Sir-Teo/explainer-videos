from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

ORDER = ["United Kingdom", "Japan", "United States", "France", "China", "South Africa", "Brazil", "India", "Mexico",
         "Bangladesh", "Nigeria", "Sub-Saharan Africa", "Ethiopia", "World"]


class World(VoiceoverScene):
    def construct(self):
        card(self, 11, "Around the world", "How many people have the system this film takes for granted?",
             "Chapter eleven. Around the world.", lit=("unit", "change"))
        self.dumbbells()

    def panel(self, key, x0, title, col):
        D = R["world"][key]
        w = 4.2
        rows = VGroup()
        axis = VGroup(*[VGroup(DashedLine([x0 + w * v / 100, 2.55, 0], [x0 + w * v / 100, -3.05, 0], stroke_color=GREY_B, stroke_width=1,
                                          stroke_opacity=0.35, dash_length=0.06), tx(f"{v}%", 12, GREY_B).move_to([x0 + w * v / 100, 2.75, 0]))
                        for v in (0, 50, 100)])
        for i, c in enumerate(ORDER):
            if c not in D:
                continue
            a, b = D[c]
            y = 2.3 - 0.4 * i
            g = VGroup()
            if a is not None:
                g.add(Line([x0 + w * a / 100, y, 0], [x0 + w * b / 100, y, 0], stroke_color=col, stroke_width=4, stroke_opacity=0.6),
                      Dot([x0 + w * a / 100, y, 0], radius=0.06, color=GREY_B))
            g.add(Dot([x0 + w * b / 100, y, 0], radius=0.08, color=col))
            rows.add(g)
        head = tx(title, 18, col, bold=True).move_to([x0 + w / 2, 3.2, 0])
        return VGroup(axis, rows, head)

    def dumbbells(self):
        W = R["world"]
        names = VGroup(*[tx(c, 14, WHITE if c != "World" else PRICE, bold=(c == "World")).move_to([-4.2, 2.3 - 0.4 * i, 0], aligned_edge=RIGHT)
                         for i, c in enumerate(ORDER)])
        pw = self.panel("SH.H2O.SMDW.ZS", -3.9, "safely managed drinking water", WATER)
        ps = self.panel("SH.STA.SMSS.ZS", 1.6, "safely managed sanitation", SEWAGE)
        key = VGroup(Dot(radius=0.06, color=GREY_B), tx("2000", 13, GREY_A), Dot(radius=0.08, color=WHITE), tx("2024", 13, GREY_A)).arrange(RIGHT, buff=0.1).to_edge(DOWN, buff=0.7).shift(RIGHT * 3)
        w, s = W["SH.H2O.SMDW.ZS"], W["SH.STA.SMSS.ZS"]
        src = source("WHO/UNICEF Joint Monitoring Programme, via the World Bank's World Development Indicators (SH.H2O.SMDW.ZS, "
                     "SH.STA.SMSS.ZS); share of the population", size=13)
        with self.voiceover(
            "Everything so far assumes the system exists. For much of the world, it is still being built. The World "
            "Health Organization and UNICEF count who has 'safely managed' water, piped or protected, available at home "
            "and clean, and safely managed sanitation, where the waste is treated or safely contained. <bookmark mark='a'/> "
            f"In 2024, about {w['World'][1]:.0f} per cent of the world's people had safely managed drinking water, up from "
            f"{w['World'][0]:.0f} per cent in 2000. India went from about {w['India'][0]:.0f} to {w['India'][1]:.0f} "
            f"per cent. <bookmark mark='b'/> Sanitation is further behind: about {s['World'][1]:.0f} per cent of the world, "
            f"up from {s['World'][0]:.0f}. China went from {s['China'][0]:.0f} to {s['China'][1]:.0f} per cent, India "
            f"from {s['India'][0]:.0f} to {s['India'][1]:.0f}. <bookmark mark='c'/> In sub-Saharan Africa, about "
            f"{s['Sub-Saharan Africa'][1]:.0f} per cent; in Ethiopia, {s['Ethiopia'][1]:.0f}. London's problem of 1858 "
            "is still, for billions of people, the problem of today, and the pipes and works that solve it are the "
            "same slow, heavy, fixed-cost machine."
        ) as vo:
            self.play(FadeIn(names), FadeIn(pw[0]), FadeIn(pw[2]), FadeIn(ps[0]), FadeIn(ps[2]), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in pw[1]], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in ps[1]], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(names[ORDER.index("Sub-Saharan Africa")], color=BAD), Indicate(names[ORDER.index("Ethiopia")], color=BAD))
        self.clear_scene()
