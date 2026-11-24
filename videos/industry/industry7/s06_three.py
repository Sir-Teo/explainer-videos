from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Three(VoiceoverScene):
    def construct(self):
        card(self, 6, "Three answers, one market", "When the methods disagree, which one is wrong?",
             "Chapter six. Three answers, one market.", lit=("unit", "dollar"))
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
        self.gate()

    def gate(self):
        """Rule 3 as a picture: which input moves the bottom-up answer most? A tornado of the game's sum."""
        from videos.industry.industry7.s02_guess import BOTTLE_L, JUG_PRICE, L_PER_GAL, PACK_BOTTLES, PACK_PRICE
        W = R["water"]
        base = dict(percap=W["percap"], single=0.71, pack=PACK_PRICE, jug=JUG_PRICE)

        def total(x):
            gal = W["pop"] * x["percap"] / 1000  # bn gallons
            per_pack = x["pack"] / (PACK_BOTTLES * BOTTLE_L / L_PER_GAL)
            return gal * (x["single"] * per_pack + (1 - x["single"]) * x["jug"])
        mid = total(base)
        ranges = [("pack price", "pack", 4.50, 8.00, "$4.50 to $8.00 for 24"),
                  ("single-serve share", "single", 0.65, 0.77, "65% to 77% of gallons"),
                  ("jug price", "jug", 1.00, 2.00, "$1.00 to $2.00 a gallon"),
                  ("gallons per person", "percap", W["percap"] * 0.95, W["percap"] * 1.05, "plus or minus 5%")]
        res = []
        for name, k, lo, hi, how in ranges:
            a, b = total({**base, k: lo}), total({**base, k: hi})
            res.append((name, how, min(a, b), max(a, b)))
        res.sort(key=lambda r_: r_[2] - r_[3])
        u = 0.42
        x0 = 0.8
        axis = Line([x0, 2.1, 0], [x0, -2.3, 0], stroke_color=WHITE, stroke_width=2)
        mt = tx(f"${mid:.0f}bn", 22, GUESS, bold=True).next_to(axis, UP, buff=0.12)
        bars = VGroup()
        for k, (name, how, lo, hi) in enumerate(res):
            y = 1.5 - 1.05 * k
            left = Rectangle(width=max((mid - lo) * u, 0.02), height=0.6, stroke_width=0, fill_color=UNITS,
                             fill_opacity=0.9).move_to([x0, y, 0], aligned_edge=RIGHT)
            right = Rectangle(width=max((hi - mid) * u, 0.02), height=0.6, stroke_width=0, fill_color=GUESS,
                              fill_opacity=0.9).move_to([x0, y, 0], aligned_edge=LEFT)
            lab = VGroup(tx(name, 19, WHITE, bold=True), tx(how, 14, GREY_B)).arrange(DOWN, aligned_edge=RIGHT,
                                                                                       buff=0.03)
            lab.move_to([x0 - 3.6, y, 0], aligned_edge=RIGHT)
            lv = tx(f"${lo:.0f}bn", 15, UNITS).next_to(left, LEFT, buff=0.1)
            hv = tx(f"${hi:.0f}bn", 15, GUESS).next_to(right, RIGHT, buff=0.1)
            bars.add(VGroup(lab, left, right, lv, hv))
        lo_all = total({**base, "pack": 4.5, "single": 0.65, "jug": 1.0, "percap": W["percap"] * 0.95})
        hi_all = total({**base, "pack": 8.0, "single": 0.77, "jug": 2.0, "percap": W["percap"] * 1.05})
        verdict = tx(f"every input at its edge: ${lo_all:.0f}bn to ${hi_all:.0f}bn. The pack price is the range.", 19,
                     GOLD, bold=True).to_edge(DOWN, buff=0.6)
        head = tx("Your sum, if each input could be different", 24, WHITE, bold=True).to_edge(UP, buff=0.45)
        tag = estimate_tag("illustrative ranges for each input", corner=DR, size=14)
        with self.voiceover(
            "The third rule deserves a picture. Go back to your own sum. <bookmark mark='a'/> It came to about "
            f"{mid:.0f} billion dollars, from four inputs. Now let each input be different, one at a time, across a "
            "range that seems fair. <bookmark mark='b'/> The pack price, from four fifty to eight dollars for "
            f"twenty-four bottles, moves the answer from {res[0][2]:.0f} to {res[0][3]:.0f} billion. "
            "<bookmark mark='c'/> The share in single-serve bottles, the jug price and the gallons per person matter "
            "much less. <bookmark mark='d'/> Set every input at its edge at once and the range runs from about "
            f"{lo_all:.0f} to {hi_all:.0f} billion. That is what a range is for: it tells you which number to go "
            "and check. Here, it is the price of a pack: the one number in your sum that you chose yourself."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(axis), FadeIn(mt))
            vo.wait_until("b")
            g = bars[0]
            self.play(FadeIn(g[0]), GrowFromEdge(g[1], RIGHT), GrowFromEdge(g[2], LEFT), FadeIn(g[3]), FadeIn(g[4]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(g[0]), GrowFromEdge(g[1], RIGHT), GrowFromEdge(g[2], LEFT),
                                                   FadeIn(g[3]), FadeIn(g[4])) for g in bars[1:]], lag_ratio=0.35),
                      run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()
