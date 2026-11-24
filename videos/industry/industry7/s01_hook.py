from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.uber()
        self.wework()
        self.title()

    def uber(self):
        U = R["uber"]
        side = 4.6
        big = Square(side, stroke_color=TAM, stroke_width=3, fill_color=TAM, fill_opacity=0.12).move_to([-2.4, -0.3, 0])
        items = [("getting around", U["mobility"], "#F6C453", f"${U['mobility']}tn"),
                 ("freight trucking", U["freight"], "#F2A65A", f"${U['freight']}tn"),
                 ("restaurant meals", U["eats"], "#E9A0C9", f"${U['eats']}tn")]
        tm = viz.treemap(items, width=side, height=side, size=20).move_to(big)
        tot = VGroup(tx("Uber's addressable market, 2019", 20, GREY_A), tx(f"${U['tam']:.1f} trillion", 40, TAM, bold=True)
                     ).arrange(DOWN, buff=0.08).next_to(big, UP, buff=0.2)
        filing = VGroup(RoundedRectangle(corner_radius=0.05, width=2.2, height=2.8, stroke_width=0, fill_color="#E8E4DA",
                                         fill_opacity=1),
                        tx("Form S-1", 22, "#1B1F27", bold=True).shift(UP * 0.95),
                        tx("Uber Technologies", 15, "#1B1F27").shift(UP * 0.55),
                        *[Line([-0.8, 0, 0], [0.8, 0, 0], stroke_color="#8C929B", stroke_width=2).shift(
                            DOWN * (0.05 + 0.22 * k)) for k in range(5)],
                        tx("11 April 2019", 14, "#4A4F5A").shift(DOWN * 1.2)).move_to([4.2, 1.2, 0])
        # Uber's own revenue as a square at the same scale: area = dollars
        s18 = side * np.sqrt(U["revenue"][2018] / (U["tam"] * 1000))
        s25 = side * np.sqrt(U["revenue"][2025] / (U["tam"] * 1000))
        r18 = Square(s18, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(big.get_corner(DL), aligned_edge=DL)
        r25 = Square(s25, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(big.get_corner(DL), aligned_edge=DL)
        rl = VGroup(tx(f"Uber's revenue, 2018: ${U['revenue'][2018]:.1f}bn", 20, WHITE),
                    tx(f"{100 * U['share_2018']:.2f}% of it", 18, GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.06).move_to([3.9, -1.4, 0])
        rl2 = VGroup(tx(f"2025: ${U['revenue'][2025]:.1f}bn", 20, WHITE),
                     tx(f"{100 * U['share_2025']:.2f}%", 18, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(
            rl, DOWN, buff=0.3, aligned_edge=LEFT)
        arrow = Arrow(rl.get_left(), r18.get_center(), buff=0.15, color=WHITE, stroke_width=3)
        src = source("Uber Technologies, Form S-1 (11 April 2019) and Forms 10-K, 2018-2025", size=13)
        with self.voiceover(
            "In April 2019, Uber filed to sell its shares to the public. <bookmark mark='a'/> Its prospectus told "
            f"investors how big its market was: {U['tam']:.1f} trillion dollars. <bookmark mark='b'/> "
            f"{U['mobility']} trillion for getting people around, {U['freight']} trillion for moving freight by "
            f"truck, and {U['eats']} trillion for restaurant meals. <bookmark mark='c'/> Draw Uber's own revenue "
            f"that year at the same scale. {U['revenue'][2018]:.1f} billion dollars: less than a tenth of one percent "
            f"of its market. <bookmark mark='d'/> By 2025 its revenue had grown five-fold, to {U['revenue'][2025]:.0f} "
            "billion, and it was still under half of one percent. Was the twelve trillion wrong? Not exactly. It "
            "answered a different question from the one most people asked."
        ) as vo:
            self.play(FadeIn(src), FadeIn(filing, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(big), FadeIn(tot), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, scale=0.95) for b_ in tm], lag_ratio=0.3), FadeOut(big), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rl), GrowFromPoint(r18, big.get_corner(DL)), GrowArrow(arrow))
            self.play(Flash(r18, color=WHITE, line_length=0.25))
            vo.wait_until("d")
            self.play(ReplacementTransform(r18, r25), FadeIn(rl2), run_time=1.6)
        self.clear_scene()

    def wework(self):
        W = R["wework"]
        crowd = VGroup(*[draw.person(0.32, color=STONE) for _ in range(60)]).arrange_in_grid(rows=4, cols=15,
                                                                                        buff=(0.06, 0.08))
        crowd.move_to([-3.6, 1.2, 0])
        ct = tx(f"{W['members']:.0f} million people who might work there", 19, GREY_A).next_to(crowd, DOWN, buff=0.15)
        desk = VGroup(Rectangle(width=1.6, height=0.12, stroke_width=0, fill_color="#C9A26B", fill_opacity=1),
                      Rectangle(width=0.1, height=0.6, stroke_width=0, fill_color="#C9A26B", fill_opacity=1).shift(
                          DOWN * 0.36 + LEFT * 0.7),
                      Rectangle(width=0.1, height=0.6, stroke_width=0, fill_color="#C9A26B", fill_opacity=1).shift(
                          DOWN * 0.36 + RIGHT * 0.7)).move_to([3.2, 1.6, 0])
        dt = tx(f"× ${W['per_employee']:,.0f} a year of office cost each", 19, GREY_A).next_to(desk, DOWN, buff=0.5)
        eq = VGroup(tx("WeWork's total opportunity, 2019", 20, GREY_A),
                    tx(f"${W['total']:.1f} trillion", 40, TAM, bold=True)).arrange(DOWN, buff=0.08).move_to([0, -1.4, 0])
        after = VGroup(tx("30 September 2019: the share sale withdrawn", 20, WHITE),
                       tx("6 November 2023: Chapter 11", 22, "#E8554E", bold=True)).arrange(DOWN, buff=0.12).to_edge(
            DOWN, buff=0.6)
        src = source("The We Company, Form S-1 (14 August 2019) and Form RW (30 September 2019); WeWork Inc., Form 8-K "
                     "(7 November 2023)", size=13)
        with self.voiceover(
            "Four months later, the office company WeWork filed its own prospectus. <bookmark mark='a'/> It counted "
            f"{W['members']:.0f} million people in its target cities who might one day work at a desk, "
            f"<bookmark mark='b'/> and multiplied by the {W['per_employee']:,.0f} dollars a year that employers there "
            f"spend on office space for each of them. <bookmark mark='c'/> Total opportunity: "
            f"{W['total']:.0f} trillion dollars. <bookmark mark='d'/> Six weeks later the share sale was withdrawn. In "
            "November 2023 the company filed for bankruptcy. Big markets are easy to write down. This part is about "
            "how to size one honestly: what to count, how to count it, and how to tell when a number is answering "
            "the wrong question."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(p_, shift=UP * 0.05) for p_ in crowd[:30]], lag_ratio=0.02),
                      run_time=1.4)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.05) for p_ in crowd[30:]], lag_ratio=0.02), FadeIn(ct),
                      run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(desk, shift=DOWN * 0.2), FadeIn(dt))
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.2))
            vo.wait_until("d")
            self.play(FadeIn(after[0]))
            self.play(FadeIn(after[1]), crowd.animate.set_opacity(0.25), eq.animate.set_opacity(0.4))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part seven: sizing a market. How big is a market, and how would anyone know?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
