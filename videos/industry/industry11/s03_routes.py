from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Routes(VoiceoverScene):
    def construct(self):
        card(self, 2, "Steel two ways", "Ore and coal in a blast furnace, or scrap and electricity in an arc furnace?",
             "Chapter two. Steel two ways.", lit=("make",))
        self.integrated()
        self.minimill()
        self.shares()

    def integrated(self):
        Q = R["routes"]
        pel = draw.pile(1.3, ORE, 90, 1).move_to([-6.0, 1.5, 0])
        coal = draw.pile(1.1, "#3A3F4A", 70, 2, "jagged").move_to([-6.0, -0.2, 0])
        scr = draw.pile(0.9, "#8B95A7", 50, 3, "jagged").move_to([-6.0, -1.8, 0])
        labs = VGroup(VGroup(tx(f"{Q['pellets']:.1f} t iron ore pellets", 16, ORE, bold=True)).next_to(pel, DOWN, buff=0.05),
                      VGroup(tx(f"{Q['coke']:.2f} t coke", 16, "#C9D3E0", bold=True),
                             tx(f"(baked from about {Q['coal']:.1f} t of coal)", 12, GREY_B)).arrange(DOWN, buff=0.02
                                                                                                 ).next_to(coal, DOWN, buff=0.05),
                      VGroup(tx(f"{Q['scrap_bof']:.1f} t scrap", 16, STEELC, bold=True)).next_to(scr, DOWN, buff=0.05))
        bf = draw.blast_furnace(3.0).move_to([-2.4, 0.0, 0])
        conv = draw.converter(1.7).move_to([2.0, -0.6, 0])
        conv.sparks.set_opacity(0)
        conv.glow.set_opacity(0)
        lad = draw.ladle(0.6).move_to([0.0, -1.8, 0])
        slab_ = draw.slab(1.3).move_to([5.0, -1.9, 0])
        one = tx("1 tonne of steel", 20, STEELC, bold=True).next_to(slab_, DOWN, buff=0.12)
        arrows = VGroup(*[Arrow(p.get_right(), bf.shell.get_left() + UP * dy, buff=0.15, color=GREY_B, stroke_width=2.5,
                                tip_length=0.12) for p, dy in ((pel, 0.6), (coal, 0.0), (scr, -0.5))])
        bf_l = VGroup(tx("Blast furnace", 20, ORE, bold=True), tx("coke burns, takes the oxygen out of the ore:", 14, GREY_A),
                      tx("molten iron, about 4-5% carbon", 14, GREY_A)).arrange(DOWN, buff=0.03).next_to(bf, UP, buff=0.1)
        cv_l = VGroup(tx("Oxygen converter", 20, HOT, bold=True), tx("Bessemer's idea, with pure oxygen:", 14, GREY_A),
                      tx("the carbon burns off in minutes", 14, GREY_A)).arrange(DOWN, buff=0.03).next_to(conv, UP, buff=0.6)
        co2 = VGroup(tx("CO2 for each tonne of steel:", 16, GREY_A), tx(f"{Q['co2']['bfbof']:.2f} t", 34, CARBON, bold=True)
                     ).arrange(DOWN, buff=0.05).move_to([5.2, 1.6, 0])
        src = source("Cleveland-Cliffs, Form 10-K 2025 (inputs per net ton of raw steel); World Steel Association, "
                     "'Climate change and the production of iron and steel' (2025)", size=13)
        with self.voiceover(
            "There are two ways to make steel. The first is Bessemer's descendant: the integrated mill. "
            "<bookmark mark='a'/> According to Cleveland-Cliffs, America's largest integrated steelmaker, a tonne of its "
            f"steel takes about {Q['pellets']:.1f} tonnes of iron ore pellets, a third of a tonne of coke, which is coal "
            f"baked in ovens, about {Q['coal']:.1f} tonnes of coal in all, and a little scrap. <bookmark mark='b'/> In the "
            "blast furnace, the burning coke strips the oxygen from the iron ore, and molten iron runs out at the "
            "bottom, carrying four or five per cent carbon. <bookmark mark='c'/> A ladle carries it to the converter, "
            "where pure oxygen is blown in, as Bessemer blew air, and the carbon burns away in minutes. "
            "<bookmark mark='d'/> Out comes steel, cast into slabs. <bookmark mark='e'/> The carbon that took the "
            f"oxygen from the ore leaves as carbon dioxide: about {Q['co2']['bfbof']:.1f} tonnes for every tonne of "
            "steel, by the steel industry's own count."
        ) as vo:
            self.play(FadeIn(src), FadeIn(bf), FadeIn(bf_l))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(pel), FadeIn(coal), FadeIn(scr), lag_ratio=0.3), FadeIn(labs), run_time=1.5)
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("b")
            self.play(*[p.animate.shift(RIGHT * 1.5).set_opacity(0) for p in (pel, coal, scr)], FadeOut(arrows), FadeOut(labs),
                      run_time=1.5)
            self.play(Flash(bf.tap[0], color=HOT, flash_radius=0.5), bf.tap.animate.scale(1.3), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(lad, shift=UP * 0.2))
            self.play(lad.animate.move_to(conv.get_bottom() + LEFT * 1.0 + DOWN * 0.1), FadeIn(conv), FadeIn(cv_l), run_time=1.5)
            self.play(FadeOut(lad), conv.sparks.animate.set_opacity(1), conv.glow.animate.set_opacity(0.4), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeOut(conv.sparks), FadeOut(conv.glow), Rotate(conv.vessel, -1.3, about_point=conv[2].get_center()),
                      run_time=1.0)
            self.play(FadeIn(slab_, shift=RIGHT * 0.3), FadeIn(one))
            vo.wait_until("e")
            self.play(FadeIn(co2, shift=DOWN * 0.1))
            self.play(Indicate(co2[1], color=CARBON))
        self.clear_scene()

    def minimill(self):
        Q = R["routes"]
        scr = draw.pile(1.6, "#8B95A7", 110, 7, "jagged").move_to([-5.0, -1.0, 0])
        sl = VGroup(tx(f"{Q['scrap_eaf']:.1f} t scrap", 18, STEELC, bold=True), tx("old cars, buildings, offcuts", 14, GREY_A)
                    ).arrange(DOWN, buff=0.03).next_to(scr, DOWN, buff=0.08)
        pyl = draw.pylon(1.6).move_to([-5.0, 1.6, 0])
        pl = tx("electricity", 18, PRICE, bold=True).next_to(pyl, RIGHT, buff=0.15)
        f = draw.eaf(2.6).move_to([0.0, -0.6, 0])
        fl = VGroup(tx("Electric arc furnace", 20, SCRAP, bold=True), tx("an arc hotter than the sun's surface melts the scrap",
                                                                         14, GREY_A)).arrange(DOWN, buff=0.03).next_to(f, DOWN,
                                                                                                                       buff=0.2)
        slab_ = draw.slab(1.3).move_to([4.4, -1.6, 0])
        one = tx("1 tonne of steel", 20, STEELC, bold=True).next_to(slab_, DOWN, buff=0.12)
        a1 = Arrow(scr.get_right(), f.get_left() + DOWN * 0.2, buff=0.2, color=GREY_B, stroke_width=2.5, tip_length=0.12)
        a2 = Arrow(pyl.get_right() + RIGHT * 1.1, f.electrodes.get_top() + LEFT * 0.2, buff=0.1, color=PRICE, stroke_width=2.5,
                   tip_length=0.12)
        a3 = Arrow(f.get_right(), slab_.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5, tip_length=0.12)
        co2 = VGroup(tx("CO2 for each tonne of steel:", 16, GREY_A), tx(f"{Q['co2']['scrapeaf']:.2f} t", 34, GOOD, bold=True),
                     tx(f"(from iron made with gas, not coal: {Q['co2']['drieaf']:.2f} t)", 13, GREY_B)).arrange(
            DOWN, buff=0.05).move_to([4.6, 1.7, 0])
        src = source("Nucor, Form 10-K 2025 (scrap per ton of steel); World Steel Association (2025)", size=13)
        with self.voiceover(
            "The second way skips the ore altogether. <bookmark mark='a'/> A minimill melts scrap: old cars, demolished "
            "buildings, the offcuts of factories. Nucor says it takes about "
            f"{Q['scrap_eaf']:.1f} tonnes of scrap, or substitutes for it, to make a tonne of steel. "
            "<bookmark mark='b'/> The furnace is a bowl with three graphite electrodes in its lid. Lower them, switch on, "
            "and an electric arc hotter than the surface of the sun melts the charge in under an hour. "
            "<bookmark mark='c'/> Pour, cast, and you have steel. <bookmark mark='d'/> Because nobody has to pull oxygen "
            f"out of ore, the carbon dioxide is far lower: about {Q['co2']['scrapeaf']:.1f} tonnes a tonne, most of it "
            "from the power station. Some electric furnaces are fed with iron made from ore using natural gas instead "
            "of coke, which sits in between."
        ) as vo:
            self.play(FadeIn(f), FadeIn(fl), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(scr, shift=UP * 0.2), FadeIn(sl), GrowArrow(a1))
            vo.wait_until("b")
            self.play(FadeIn(pyl), FadeIn(pl), GrowArrow(a2))
            self.play(f.electrodes.animate.shift(DOWN * 0.35), run_time=0.8)
            for _ in range(3):
                self.play(f.arc.animate.scale(1.25).set_opacity(1), run_time=0.35)
                self.play(f.arc.animate.scale(1 / 1.25).set_opacity(0.7), run_time=0.35)
            vo.wait_until("c")
            self.play(GrowArrow(a3), FadeIn(slab_, shift=RIGHT * 0.2), FadeIn(one))
            vo.wait_until("d")
            self.play(FadeIn(co2, shift=DOWN * 0.1))
        self.clear_scene()

    def shares(self):
        Q = R["routes"]
        e = Q["eaf"]
        order = ["china", "japan", "korea", "world", "eu", "india", "us", "turkiye"]
        names = {"china": "China", "japan": "Japan", "korea": "South Korea", "world": "World", "eu": "EU", "india": "India",
                 "us": "United States", "turkiye": "Türkiye"}
        bars = VGroup()
        for i, k in enumerate(order):
            y = 2.2 - 0.62 * i
            w_ = 7.0 * e[k] / 100
            bg = Rectangle(width=7.0, height=0.42, stroke_width=0, fill_color=ORE, fill_opacity=0.5).move_to([-3.6, y, 0],
                                                                                                       aligned_edge=LEFT)
            fg = Rectangle(width=w_, height=0.42, stroke_width=0, fill_color=SCRAP, fill_opacity=0.95).move_to([-3.6, y, 0],
                                                                                                         aligned_edge=LEFT)
            nm = tx(names[k], 17, WHITE if k != "world" else PRICE, bold=k in ("world", "us", "china")).next_to(bg, LEFT, buff=0.2)
            v = tx(f"{e[k]:.0f}%", 15, WHITE, bold=True).next_to(fg, RIGHT, buff=0.08) if e[k] < 85 else tx(
                f"{e[k]:.0f}%", 15, "#0E1117", bold=True).move_to(fg.get_right() + LEFT * 0.35)
            bars.add(VGroup(bg, fg, nm, v))
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=SCRAP, fill_opacity=0.95), tx("electric furnace", 14, SCRAP)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_width=0, fill_color=ORE, fill_opacity=0.5), tx("blast furnace and converter",
                                                                                               14, ORE)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).next_to(bars, DOWN, buff=0.3)
        head = tx("How each country makes its steel, 2025", 24, WHITE, bold=True).to_edge(UP, buff=0.35)
        us = VGroup(tx("In the United States:", 19, WHITE, bold=True),
                    tx(f"{Q['us_integrated']:.0f} companies", 26, ORE, bold=True), tx("with blast furnaces", 15, ORE),
                    tx(f"{Q['us_minimills']:.0f} minimills", 26, SCRAP, bold=True),
                    tx(f"of {Q['us_minimill_cos']:.0f} companies", 15, SCRAP)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.6, 0.0, 0])
        src = source("World Steel Association, World Steel in Figures 2026; USGS, Mineral Commodity Summaries 2026", size=13)
        with self.voiceover(
            "Which way a country makes its steel depends on what it has. <bookmark mark='a'/> China makes almost nine "
            "tenths of its steel from ore, in blast furnaces. So do Japan and South Korea. <bookmark mark='b'/> Worldwide, "
            f"about {e['world']:.0f} per cent comes from electric furnaces. <bookmark mark='c'/> But in the United States "
            f"it is {e['us']:.0f} per cent, and in Türkiye more still. <bookmark mark='d'/> The difference is scrap. An "
            "old industrial country is a mine of old steel: cars reach the end of their lives, buildings come down, and "
            f"American scrapyards recycle almost all of it. In the United States, just {Q['us_integrated']:.0f} companies "
            f"still run blast furnaces; {Q['us_minimill_cos']:.0f} companies run {Q['us_minimills']:.0f} minimills. A "
            "country that has only just built its cities, like China, has not yet had time to throw much steel away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), *[FadeIn(VGroup(b[0], b[2])) for b in bars])
            vo.wait_until("a")
            self.play(*[GrowFromEdge(bars[i][1], LEFT) for i in range(3)], *[FadeIn(bars[i][3]) for i in range(3)])
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[3][1], LEFT), FadeIn(bars[3][3]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(bars[i][1], LEFT) for i in range(4, 8)], *[FadeIn(bars[i][3]) for i in range(4, 8)])
            vo.wait_until("d")
            self.play(FadeIn(us, shift=UP * 0.1))
        self.clear_scene()
