from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403

# The landscape: (link, [(company, region)]), most important first.  Companies named from their filings, Apple's
# supplier list and the trackers' rankings; a company's place in a row is not a claim about its share.
MAP = [
    ("Phone brands", [("Apple", "US"), ("Samsung", "Korea"), ("Xiaomi", "China"), ("vivo", "China"),
                      ("OPPO", "China"), ("Transsion", "China"), ("Honor", "China"), ("Huawei", "China"),
                      ("Google", "US")]),
    ("Processor design", [("Apple", "US"), ("Qualcomm", "US"), ("MediaTek", "Taiwan"), ("Samsung", "Korea"),
                          ("HiSilicon (Huawei)", "China"), ("UNISOC", "China"), ("Arm: the designs licensed", "Europe")]),
    ("Chip making", [("TSMC", "Taiwan"), ("Samsung Foundry", "Korea"), ("SMIC", "China"),
                     ("ASML: the machines", "Europe")]),
    ("Memory", [("Samsung", "Korea"), ("SK hynix", "Korea"), ("Micron", "US"), ("Kioxia", "Japan"),
                ("CXMT", "China"), ("YMTC", "China")]),
    ("Displays", [("Samsung Display", "Korea"), ("LG Display", "Korea"), ("BOE", "China"), ("TCL CSOT", "China"),
                  ("Visionox", "China")]),
    ("Cameras", [("Sony", "Japan"), ("Samsung", "Korea"), ("OmniVision", "China"), ("LG Innotek", "Korea"),
                 ("Sunny Optical", "China"), ("Largan", "Taiwan")]),
    ("Modems and radios", [("Qualcomm", "US"), ("Broadcom", "US"), ("Murata", "Japan"), ("Skyworks", "US"),
                           ("Qorvo", "US"), ("MediaTek", "Taiwan")]),
    ("Assembly", [("Foxconn", "Taiwan"), ("Luxshare", "China"), ("Tata Electronics", "India"),
                  ("BYD Electronics", "China"), ("Pegatron", "Taiwan"), ("Dixon", "India")]),
]


class Map(VoiceoverScene):
    def construct(self):
        card(self, 14, "The landscape", "Who are the companies, and where are they?",
             "Chapter fourteen. The landscape.", lit=("moat",))
        self.grid()

    def grid(self):
        rows = VGroup()
        for link, cos in MAP:
            name = TB(link, 20, I.TEXT)
            ps = VGroup(*[pill(c, region=r, size=17) for c, r in cos]).arrange(RIGHT, buff=0.1)
            if ps.width > 10.5:
                ps.scale_to_fit_width(10.5)
            rows.add(VGroup(name, ps))
        lens = VGroup(RoundedRectangle(corner_radius=0.06, width=0.5, height=0.36, stroke_width=0, fill_color="#5B6372",
                                       fill_opacity=1), Circle(radius=0.12, stroke_color=I.CAMERA, stroke_width=3,
                                                               fill_color="#101722", fill_opacity=1))
        screen = VGroup(RoundedRectangle(corner_radius=0.05, width=0.5, height=0.34, stroke_color="#C9D3E0",
                                         stroke_width=2, fill_color=I.DISPLAY, fill_opacity=0.8))
        mast = VGroup(Line(DOWN * 0.2, UP * 0.2, stroke_color=I.RF, stroke_width=3),
                      *[Arc(radius=r_, start_angle=-0.6, angle=1.2, stroke_color=I.RF, stroke_width=2).move_arc_center_to(
                          UP * 0.2) for r_ in (0.12, 0.22)],
                      *[Arc(radius=r_, start_angle=PI - 0.6, angle=1.2, stroke_color=I.RF, stroke_width=2).move_arc_center_to(
                          UP * 0.2) for r_ in (0.12, 0.22)])
        glyphs = [viz.phone(0.5, back=True, body=BODY_17), draw.chip(0.42, color=I.CHIP), draw.wafer(0.21, die=0.05),
                  draw.chip(0.42, color=I.MEMORY), screen, lens, mast, draw.factory(0.55, color=I.ASSEMBLY)]
        for i, r in enumerate(rows):
            y = 2.55 - 0.66 * i
            r[0].move_to(np.array([-4.15, y, 0]), aligned_edge=RIGHT)
            r[1].move_to(np.array([-3.9, y, 0]), aligned_edge=LEFT)
            g_ = glyphs[i]
            g_.scale_to_fit_height(min(g_.height, 0.46))
            g_.move_to(np.array([r[0].get_left()[0] - 0.4, y, 0]))
            r[0].add(g_)
        legend = VGroup(*[VGroup(Dot(radius=0.07, color=REGION[k]), T(REGION_NAME[k] if k != "China" else "China", 16,
                                                                          I.DIM)).arrange(RIGHT, buff=0.08)
                          for k in ("US", "China", "Taiwan", "Korea", "Japan", "India", "Europe")]
                        ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        stamp = as_of("as of November 2026")
        src = source("company filings; Apple Supplier List; IDC and Counterpoint rankings", corner=UL)
        def show(i):
            return AnimationGroup(FadeIn(rows[i][0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.08) for p in rows[i][1]],
                                                                  lag_ratio=0.12))
        with self.voiceover(
            "Here is the industry on one page, as of November 2026: each link of the chain, and the companies that "
            "matter in it, coloured by where they are based. <bookmark mark='a'/> The brands: Apple and Samsung, then "
            "a crowd of Chinese makers, and Google. <bookmark mark='b'/> The processors are designed by Apple, "
            "Qualcomm, MediaTek in Taiwan and a few others, almost all on instruction sets licensed from Arm, a "
            "British company. <bookmark mark='c'/> They are made by very few: TSMC above all, Samsung, and in China "
            "SMIC, on machines whose most advanced versions only ASML, in the Netherlands, can build. <bookmark "
            "mark='d'/> Memory: three big makers, Samsung, SK hynix and Micron, plus Kioxia in flash storage and two "
            "Chinese challengers, CXMT and YMTC. <bookmark mark='e'/> Displays: the two Korean leaders and BOE of "
            "China. <bookmark mark='f'/> Cameras: Sony leads in image sensors, with Samsung and OmniVision behind it. "
            "<bookmark mark='g'/> Modems and radio parts: mostly American and Japanese companies. <bookmark mark='h'/> "
            "And assembly: Taiwanese, Chinese and now Indian contract manufacturers. <bookmark mark='i'/> Two things "
            "stand out. The rows where very few names appear, making the chips and making memory, are the rows where "
            "the margins were highest in chapter seven and chapter twelve. And Chinese companies appear in almost every "
            "row; what China lacks is the most advanced chip making. Since American export rules cut Huawei off "
            "from TSMC in 2020, its phones have run on processors made by SMIC on an older process."
        ) as vo:
            self.play(FadeIn(stamp), FadeIn(src), FadeIn(legend))
            for i, m in enumerate("abcdefgh"):
                vo.wait_until(m)
                self.play(show(i), run_time=1.2)
            vo.wait_until("i")
            self.play(Indicate(rows[2][1], color=I.CHIP, scale_factor=1.04), Indicate(rows[3][1], color=I.MEMORY,
                                                                                         scale_factor=1.04))
        self.clear_scene()
