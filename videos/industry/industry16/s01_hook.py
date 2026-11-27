from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.shih()
        self.two()
        self.title()

    def shih(self):
        H = R["hook"]
        ax = VGroup(Arrow([-5.2, -2.4, 0], [5.4, -2.4, 0], buff=0, stroke_width=3, color=GREY_B, max_tip_length_to_length_ratio=0.03),
                    Arrow([-5.2, -2.4, 0], [-5.2, 2.0, 0], buff=0, stroke_width=3, color=GREY_B, max_tip_length_to_length_ratio=0.05))
        yl = tx("value added", 15, GREY_B).rotate(PI / 2).next_to(ax[1], LEFT, buff=0.12)
        curve = smile(9.6, 3.6).move_to([0.1, 0.0, 0]).set_stroke(PRICE, 6)
        stages = VGroup(tx("research,", 16, PARTS, bold=True), tx("components", 16, PARTS, bold=True)).arrange(DOWN, buff=0.03).move_to([-4.0, -2.85, 0])
        mid = tx("manufacturing", 16, ASSEMBLER, bold=True).move_to([0.1, -2.85, 0])
        right = VGroup(tx("brand,", 16, BRAND, bold=True), tx("service", 16, BRAND, bold=True)).arrange(DOWN, buff=0.03).move_to([4.3, -2.85, 0])
        dots = VGroup(Dot(curve.point_from_proportion(0.04), radius=0.11, color=PARTS), Dot(curve.point_from_proportion(0.5), radius=0.11, color=ASSEMBLER),
                      Dot(curve.point_from_proportion(0.96), radius=0.11, color=BRAND))
        quote = VGroup(tx("'as I drew the curve of the value added that I analyzed,", 15, WHITE),
                       tx("it turned out to result in a smile-shaped curve.'", 15, WHITE),
                       tx("Stan Shih, founder of Acer, on 1992 (oral history, 2011)", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).to_corner(UL, buff=0.4)
        q2 = tx("'The curve showed manufacturing is the lowest in terms of value.'", 15, ASSEMBLER).move_to([0.6, 1.3, 0])
        tag = estimate_tag("Shih's curve, redrawn: a sketch, not data", corner=DR, size=12)
        src = source("Computer History Museum, oral history of Stan Shih, recorded 21 March 2011 (CHM X6261.2012), p. 31", size=13)
        with self.voiceover(
            f"In {H['shih']:.0f} Stan Shih, the founder of Acer, the Taiwanese computer maker, sat down to work out where the "
            "money in his industry was made. <bookmark mark='a'/> He went link by link: the operating system, the processor, "
            "the memory and the drives at one end; putting the computer together in the middle; the brand, the selling and "
            "the service at the other. <bookmark mark='b'/> 'As I drew the curve of the value added that I analyzed,' he "
            "said, 'it turned out to result in a smile-shaped curve.' <bookmark mark='c'/> High at both ends. And in the "
            "middle, the lowest point: 'The curve showed manufacturing is the lowest in terms of value.' He drew it to "
            "persuade his own staff that moving assembly out of Taiwan would cost them nothing that mattered."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(src), FadeIn(tag), FadeIn(ghost(curve, opacity=0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(stages, shift=UP * 0.1), FadeIn(mid, shift=UP * 0.1), FadeIn(right, shift=UP * 0.1), lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(quote), Create(curve), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), FadeIn(q2, shift=DOWN * 0.1))
            self.play(Indicate(dots[1], color=ASSEMBLER, scale_factor=1.6))
        self.clear_scene()

    def two(self):
        H, B = R["hook"], R["brand"]
        sc = 0.016
        y1, y2 = 1.2, -1.4
        hh_rev = Rectangle(width=H["hh_rev_usd"] * sc, height=0.8, stroke_width=0, fill_color=ASSEMBLER, fill_opacity=0.35).move_to([-5.0, y1, 0], aligned_edge=LEFT)
        hh_ni = Rectangle(width=H["hh_ni_usd"] * sc, height=0.8, stroke_width=0, fill_color=ASSEMBLER, fill_opacity=1).move_to([-5.0, y1, 0], aligned_edge=LEFT)
        ap_rev = Rectangle(width=B["rev"] * sc, height=0.8, stroke_width=0, fill_color=BRAND, fill_opacity=0.35).move_to([-5.0, y2, 0], aligned_edge=LEFT)
        ap_ni = Rectangle(width=B["ni"] * sc, height=0.8, stroke_width=0, fill_color=BRAND, fill_opacity=1).move_to([-5.0, y2, 0], aligned_edge=LEFT)
        l1 = VGroup(tx("Hon Hai (Foxconn), 2025", 18, WHITE, bold=True),
                    tx(f"revenue NT${H['hh_rev_twd'] / 1000:.1f} trillion, about ${H['hh_rev_usd']:.0f}bn", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(hh_rev, UP, buff=0.1).align_to(hh_rev, LEFT)
        l2 = VGroup(tx("Apple, fiscal 2026", 18, WHITE, bold=True), tx(f"revenue ${B['rev']:.0f}bn", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).next_to(ap_rev, UP, buff=0.1).align_to(ap_rev, LEFT)
        k1 = tx(f"kept: {100 * H['hh_kept']:.1f} cents in the dollar", 17, ASSEMBLER, bold=True).next_to(hh_rev, RIGHT, buff=0.2)
        k2 = tx(f"kept: {100 * B['ni'] / B['rev']:.0f} cents in the dollar", 17, BRAND, bold=True).next_to(ap_rev, RIGHT, buff=0.2)
        src = source("Hon Hai, audited consolidated statements 2025 (RNS, 3 August 2026); Apple, Form 10-K FY2026; Federal Reserve, "
                     f"NT$ {H['twd']:.2f} to the dollar (2025 average)", size=12)
        with self.voiceover(
            "Thirty-four years later the curve can be read straight from two sets of accounts. <bookmark mark='a'/> Hon Hai "
            "of Taiwan, better known as Foxconn, makes phones, servers and computers for other companies' brands. In 2025 its "
            f"revenue was NT${H['hh_rev_twd'] / 1000:.1f} trillion, about ${H['hh_rev_usd']:.0f} billion. "
            f"<bookmark mark='b'/> It kept {100 * H['hh_kept']:.1f} cents of every dollar as profit. <bookmark mark='c'/> "
            f"Apple, which designs devices and has them made by partners like Hon Hai, had ${B['rev']:.0f} billion of "
            f"revenue in its latest year, <bookmark mark='d'/> and kept {100 * B['ni'] / B['rev']:.0f} cents of every dollar. "
            "The company that builds the device takes in a fortune and keeps almost none of it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(l1), FadeIn(ghost(hh_rev, ap_rev, opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(hh_rev, LEFT), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(hh_ni, LEFT), FadeIn(k1, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(l2), GrowFromEdge(ap_rev, LEFT), run_time=1.5)
            vo.wait_until("d")
            self.play(GrowFromEdge(ap_ni, LEFT), FadeIn(k2, shift=LEFT * 0.1))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover(
            "Industry, Built. Part sixteen: electronics. Why does the company that builds the device keep the least of it?"
        ):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
