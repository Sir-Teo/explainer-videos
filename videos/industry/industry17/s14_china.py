from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

EXPORTERS = ["Germany", "China", "Japan", "South Korea", "Mexico", "United States"]


class China(VoiceoverScene):
    def construct(self):
        card(self, 12, "China", "How did China come to export more cars than Japan?",
             "Chapter twelve. China. How did China come to export more cars than Japan?",
             lit=("change", "moat"))
        self.exports()
        self.home()
        self.walls()

    def exports(self):
        C = R["china"]
        X = C["exports"]
        pa = viz.plot_axes([2015, 2025.5], [0, 200], x_length=8.4, y_length=4.4, xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                           yticks=[0, 50, 100, 150, 200], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="exports of passenger cars, US$ billion (as each country reports them)", size=13).move_to([-1.2, -0.5, 0])
        lines, labs = VGroup(), VGroup()
        for c in EXPORTERS:
            s = {y: v for y, v in X[c].items() if 2015 <= y <= 2025}
            col = COUNTRY_COL[c]
            lines.add(poly(pa, sorted(s.items()), col, 5 if c == "China" else 3))
            nudge = {"China": 0.17, "Japan": -0.17, "South Korea": 0.08, "Mexico": 0.05, "United States": -0.17}.get(c, 0.0)
            labs.add(tx(f"{c} ${s[2025]:.0f}bn", 15, col, bold=True).next_to(pa.ax.c2p(2025, s[2025]), RIGHT, buff=0.12).shift(UP * nudge))
        ci = EXPORTERS.index("China")
        ship_ = draw.car_carrier(2.0).to_corner(UR, buff=0.5).shift(LEFT * 0.3)
        src = source("UN Comtrade: exports of HS 8703 to the world, as reported by each exporter", size=12)
        with self.voiceover(
            "Now the third arrival. <bookmark mark='a'/> These are the world's big car exporters, by the value of the "
            "passenger cars they ship abroad. Germany leads, then Japan; South Korea, Mexico and the United States "
            "follow. <bookmark mark='b'/> And this is China. In 2015 it exported "
            f"{X['China'][2015]:.0f} billion dollars' worth of cars. In 2020, {X['China'][2020]:.0f}. <bookmark mark='c'/> "
            f"In 2025, {X['China'][2025]:.0f} billion, more by value than Japan, and second only to Germany: "
            f"{X['China'][2025] / X['China'][2015]:.0f} times as much in ten years."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ship_), FadeIn(ghost(lines, opacity=0.25)))
            vo.wait_until("a")
            self.play(*[Create(lines[i]) for i in range(len(EXPORTERS)) if i != ci], run_time=2.5)
            self.play(*[FadeIn(labs[i]) for i in range(len(EXPORTERS)) if i != ci])
            vo.wait_until("b")
            self.play(Create(lines[ci]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(labs[ci]), Indicate(lines[ci], color=COUNTRY_COL["China"]))
        self.clear_scene()

    def home(self):
        C = R["china"]
        B = C["byd"]
        get("tm.china")
        big = VGroup(tx("China, 2025", 20, WHITE, bold=True),
                     tx(f"{C['total']:.1f} million vehicles sold", 30, COUNTRY_COL["China"], bold=True),
                     tx(f"{C['nev']:.1f} million new energy vehicles: {100 * C['share']:.1f}%", 20, EV, bold=True),
                     tx(f"more than {C['export']:.0f} million exported, {C['nev_export']:.1f} million of them electric", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.4, 1.3, 0])
        byd = VGroup(tx("BYD, 2025", 20, WHITE, bold=True), tx(f"{B['nev']:.1f} million new energy vehicles", 17, GREY_A),
                     tx(f"revenue about ${B['rev']:.0f}bn", 17, GREY_A),
                     tx(f"kept {100 * B['margin']:.1f} cents in the dollar, profit down 19%", 17, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.4, -1.5, 0])
        gm = VGroup(tx("GM's share of China", 17, MAKER, bold=True), tx(f"2023 {C['gm_share'][0]:.1f}%  ->  2025 {C['gm_share'][1]:.1f}%", 20, MAKER, bold=True)).arrange(DOWN, buff=0.06).move_to([3.4, 1.3, 0])
        quote = VGroup(tx("Toyota, Form 20-F: 'In China, ... consumption", 15, WHITE), tx("growth remained sluggish due to continued", 15, WHITE),
                       tx("price stagnation and intense price competition.'", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.4, -1.3, 0])
        src = source("CAAM via Xinhua (14 January 2026); BYD, 2025 annual results (HKEX); GM, Form 10-K 2025; Toyota, Form 20-F", size=12)
        with self.voiceover(
            "The exports grew out of the biggest car market in the world. <bookmark mark='a'/> According to China's "
            f"carmakers' association, China sold {C['total']:.1f} million vehicles in 2025, and {100 * C['share']:.0f} per "
            "cent of them were what China calls new energy vehicles: battery cars and plug-in hybrids. "
            f"<bookmark mark='b'/> BYD alone sold {B['nev']:.1f} million. But look at what it kept: "
            f"{100 * B['margin']:.1f} cents in the dollar, and its profit fell by a fifth. <bookmark mark='c'/> The "
            f"foreign makers are losing ground: General Motors' share of China fell from {C['gm_share'][0]:.1f} to "
            f"{C['gm_share'][1]:.1f} per cent in two years. <bookmark mark='d'/> Toyota's annual report describes China's "
            "market in four words: intense price competition. Many makers, each with plants to fill, each tempted to cut "
            "its price to fill them: it looks like the showroom duel from the start of this film, played on a national "
            "scale, and exports are one place for the extra cars to go."
        ) as vo:
            self.play(FadeIn(src), FadeIn(big[0]), FadeIn(byd[0]), FadeIn(gm[0]), FadeIn(ghost(big[1:], byd[1:], gm[1], opacity=0.4)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in big[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in byd[1:]], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(gm[1]))
            vo.wait_until("d")
            self.play(FadeIn(quote))
        self.clear_scene()

    def walls(self):
        C = R["china"]
        eu = C["eu"]
        us = VGroup(tx("United States", 20, COUNTRY_COL["United States"], bold=True),
                    tx(f"{C['ustr']:.0f}%", 64, BAD, bold=True), tx("extra duty on Chinese electric cars,", 15, GREY_A),
                    tx("from 27 September 2024 (Section 301)", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([-4.0, 0.4, 0])
        names = [("byd", "BYD"), ("geely", "Geely"), ("other", "other cooperating makers"), ("saic", "SAIC"), ("tesla", "Tesla (Shanghai)")]
        rows = VGroup()
        for i, (k, n) in enumerate(sorted(names, key=lambda kn: -eu[kn[0]])):
            y = 1.5 - 0.6 * i
            b = bar(1.4, y, eu[k] * 0.1, 0.38, BAD)
            rows.add(VGroup(tx(n, 15, WHITE).next_to([1.25, y, 0], LEFT, buff=0.0), b, tx(f"{eu[k]:.1f}%", 15, BAD, bold=True).next_to(b, RIGHT, buff=0.1)))
        eh = tx("European Union: extra duty on electric cars from China, by maker", 17, COUNTRY_COL["Europe"], bold=True).move_to([2.6, 2.3, 0])
        wall = VGroup(*[Rectangle(width=0.5, height=0.25, stroke_color="#0E1117", stroke_width=1, fill_color="#8A5A44", fill_opacity=1)
                        .move_to([-6.2 + 0.52 * (i % 3) + (0.26 if (i // 3) % 2 else 0), -2.4 + 0.27 * (i // 3), 0]) for i in range(15)])
        src = source("USTR, 89 FR 76581 (18 September 2024); European Commission Implementing Regulation (EU) 2024/2754 (29 October 2024)", size=12)
        with self.voiceover(
            "The rest of the world has answered with tariffs. <bookmark mark='a'/> In September 2024 the United States raised "
            f"its duty on electric cars from China to {C['ustr']:.0f} per cent. <bookmark mark='b'/> A month later the "
            "European Union, after an investigation into Chinese subsidies, set extra duties maker by maker: "
            f"{eu['saic']:.1f} per cent for SAIC, {eu['geely']:.1f} for Geely, {eu['byd']:.1f} for BYD, and "
            f"{eu['tesla']:.1f} for Tesla's Shanghai plant. <bookmark mark='c'/> Duties raise the price of a Chinese "
            "car abroad. They do not close the plants at home, so the pressure on prices stays in China, and in every "
            "market without a wall."
        ) as vo:
            self.play(FadeIn(src), FadeIn(us[0]), FadeIn(eh), FadeIn(wall), FadeIn(ghost(us[1:], rows, opacity=0.4)))
            vo.wait_until("a")
            self.play(FadeIn(us[1:]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(us[1], color=BAD))
        self.clear_scene()
