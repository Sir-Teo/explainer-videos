from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Three(VoiceoverScene):
    def construct(self):
        card(self, 5, "Three answers, one market", "When the methods disagree, which one is wrong?",
             "Chapter five. Three answers, one market.", lit=("unit", "dollar"))
        W = R["water"]
        line = NumberLine(x_range=[0, 32, 4], length=11.0, include_numbers=False, color=GREY_B).move_to([0, -0.4, 0])
        ticks = VGroup(*[tx(f"${v}bn", 15, GREY_B).next_to(line.n2p(v), DOWN, buff=0.15) for v in (0, 8, 16, 24, 32)])
        pts = [(W["census"], FACTORY, "factory gate", "Census, US plants filed as bottled water"),
               (W["primo"], RETAIL, "retail", "Primo's 10-K, still, sparkling and seltzer"),
               (28.0, GUESS, "retail, bottom-up", "your sum: gallons × shelf prices")]
        marks = VGroup()
        for k, (v, col, lab, how) in enumerate(pts):
            d = glow_dot(line.n2p(v), color=col, radius=0.13)
            t_ = VGroup(tx(lab, 19, col, bold=True), tx(how, 14, GREY_B)).arrange(DOWN, buff=0.04)
            t_.next_to(d, UP if k != 1 else DOWN, buff=0.35 if k != 1 else 0.7)
            if k == 2:
                t_.shift(RIGHT * 0.6)
            marks.add(VGroup(d, t_))
        band = Rectangle(width=line.n2p(28)[0] - line.n2p(W["primo"])[0] + 0.4, height=0.5, stroke_width=0,
                         fill_color=RETAIL, fill_opacity=0.18).move_to((line.n2p(W["primo"]) + line.n2p(28)) / 2)
        bt = tx("US bottled water at retail, 2023: roughly $25-28bn", 22, WHITE, bold=True).to_edge(UP, buff=0.7)
        fac = tx(f"at the factory gate, US bottled-water plants only: ${W['census']:.1f}bn", 18, FACTORY).next_to(
            bt, DOWN, buff=0.2)
        rules = VGroup(tx("Rules for triangulating", 22, GOLD, bold=True),
                       tx("1. put every estimate on the same definition before comparing", 17, WHITE),
                       tx("2. if two methods agree, check they do not share an input", 17, WHITE),
                       tx("3. report a range, and say what the edges depend on", 17, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.45)
        src = source("Census Bureau (AIES); Primo Brands, Form 10-K; Beverage Marketing Corporation; this film's sum",
                     size=13)
        with self.voiceover(
            "Put the three answers on one line. <bookmark mark='a'/> The Census, at the factory gate. "
            "<bookmark mark='b'/> Primo's figure, at the till. <bookmark mark='c'/> Your sum, from the gallons and "
            "the shelf prices, also at the till. <bookmark mark='d'/> Once each is put on the same definition, two of "
            "them agree to within a few billion dollars: American bottled water sold at retail for something like "
            "twenty-five to twenty-eight billion dollars in 2023. The Census figure is not wrong. It answers a "
            "different question: what American bottled-water plants were paid for what they made. "
            "<bookmark mark='e'/> That is triangulation. Put every estimate on the same definition before comparing "
            "them. When two methods agree, check that they do not secretly share an input: yours rests on the "
            "tracker's count of gallons, and Primo does not say where its number comes from. And report a range, "
            "with what its edges depend on, rather "
            "than one number with false precision."
        ) as vo:
            self.play(FadeIn(src), Create(line), FadeIn(ticks))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(marks[k][0], scale=2), FadeIn(marks[k][1], shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(band), FadeIn(bt), FadeIn(fac))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rules], lag_ratio=0.4), run_time=2.4)
        self.clear_scene()
