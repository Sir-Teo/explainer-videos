from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry2.common import *  # noqa: F403


class Revenue(VoiceoverScene):
    def construct(self):
        card(self, 2, "Sales count the same dollar again", "Why is a medicine wholesaler as big as Apple?",
             "Chapter two. Sales count the same dollar again.", lit=("dollar",))
        self.two()
        self.chain()

    def two(self):
        M = R["companies"]["mck"]
        apple_rev, apple_gp = get("rev.apple.fy2025"), get("gp.apple.fy2025")
        sc = 4.4 / max(M["rev"], apple_rev)
        base = DOWN * 2.1

        def col(x, rev, gp, name, c):
            r = Rectangle(width=1.5, height=sc * rev, fill_color=c, fill_opacity=0.22, stroke_color=c, stroke_width=2)
            g = Rectangle(width=1.5, height=max(sc * gp, 0.04), fill_color=I.PROFIT, fill_opacity=0.9, stroke_width=0)
            r.move_to(base + RIGHT * x, aligned_edge=DOWN)
            g.move_to(base + RIGHT * x, aligned_edge=DOWN)
            lr = VGroup(TB(f"${rev:.0f}bn", 24, c), T("sales", 16, I.DIM)).arrange(DOWN, buff=0.03).next_to(r, UP, buff=0.1)
            lg = VGroup(TB(f"${gp:.1f}bn", 24, I.PROFIT), T(f"left after paying suppliers ({100 * gp / rev:.1f}%)", 16,
                        I.DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).next_to(g, RIGHT, buff=0.2).align_to(g, DOWN)
            nm = TB(name, 26, I.TEXT).next_to(r, DOWN, buff=0.2)
            return VGroup(r, g, lr, lg, nm)
        mck = col(-3.6, M["rev"], M["gp"], "McKesson", "#4FD1C5")
        apl = col(1.6, apple_rev, apple_gp, "Apple", "#E8EAED")
        src = source("McKesson Form 10-K FY2026; Apple Form 10-K FY2025")
        with self.voiceover(
            "Why does a medicine wholesaler sell as much as Apple? <bookmark mark='a'/> McKesson buys medicines from "
            "the drug makers and delivers them to pharmacies and hospitals. In its last fiscal year its sales were "
            "403 billion dollars. <bookmark mark='b'/> But almost all of that was the price of the medicines it "
            "bought. What was left after paying its suppliers was 14.6 billion dollars, three and a half cents of "
            "each dollar. <bookmark mark='c'/> Apple's sales were about the same, 416 billion dollars, <bookmark "
            "mark='d'/> and what was left after paying for its parts and its factories was 195 billion: almost half. "
            "Measured by sales, the two companies are the same size. Measured by what each adds, Apple is thirteen "
            "times bigger."
        ) as vo:
            buyers = VGroup(draw.crowd(6, 0.38, cols=3), T("customers", 16, I.DIM)).arrange(DOWN, buff=0.08).move_to(
                [-6.2, 2.6, 0])
            makers = VGroup(draw.factory(1.0, color="#B58CFF"), T("drug makers", 16, I.DIM)).arrange(DOWN, buff=0.06
                                                                                                    ).move_to([-1.0, 2.75, 0])
            parts = VGroup(draw.factory(1.0, color="#8FA3BF"), T("parts makers", 16, I.DIM)).arrange(DOWN, buff=0.06
                                                                                                   ).move_to([4.7, 2.75, 0])

            def pour(col_, n):
                coins, a = draw.coin_flow(buyers.get_right(), col_[0].get_center() + UP * 0.6, n=n, r=0.1, arc=-0.6)
                self.add(coins)
                return coins, a

            def pay_out(coins, k, dst):
                go = coins[:k]
                return [MoveAlongPath(c, ArcBetweenPoints(c.get_center(), dst, angle=-0.6)) for c in go]
            self.play(FadeIn(src), FadeIn(buyers))
            vo.wait_until("a")
            cm, am = pour(mck, 10)
            self.play(am, GrowFromEdge(mck[0], DOWN), FadeIn(mck[2]), FadeIn(mck[4]), FadeIn(makers), run_time=1.8)
            vo.wait_until("b")
            self.play(LaggedStart(*pay_out(cm, 9, makers.get_bottom()), lag_ratio=0.1), run_time=1.6)
            self.remove(*cm[:9])
            self.play(GrowFromEdge(mck[1], DOWN), FadeIn(mck[3]), cm[9].animate.move_to(mck[1].get_top() + UP * 0.2))
            vo.wait_until("c")
            ca, aa = pour(apl, 10)
            self.play(aa, GrowFromEdge(apl[0], DOWN), FadeIn(apl[2]), FadeIn(apl[4]), FadeIn(parts), run_time=1.8)
            vo.wait_until("d")
            self.play(LaggedStart(*pay_out(ca, 5, parts.get_bottom()), lag_ratio=0.1), run_time=1.4)
            self.remove(*ca[:5])
            self.play(GrowFromEdge(apl[1], DOWN), FadeIn(apl[3]),
                      *[c.animate.move_to(apl[1].get_top() + UP * 0.2 + RIGHT * (0.22 * k - 0.44))
                        for k, c in enumerate(ca[5:])])
        self.clear_scene()

    def chain(self):
        links = [("Drug maker", 100, "#B58CFF"), ("Wholesaler", 104, "#4FD1C5"), ("Pharmacy", 125, "#F2A65A")]
        boxes = VGroup()
        for name, v, c in links:
            b = RoundedRectangle(corner_radius=0.12, width=2.8, height=1.3, fill_color=c, fill_opacity=0.14,
                                 stroke_color=c, stroke_width=2)
            boxes.add(VGroup(b, VGroup(T(name, 22, I.TEXT), TB(f"sells for ${v}", 26, c)).arrange(DOWN, buff=0.08
                                                                                                  ).move_to(b)))
        boxes.arrange(RIGHT, buff=0.9).shift(UP * 1.2)
        arrows = VGroup(*[viz.arrow_line(boxes[i].get_right(), boxes[i + 1].get_left()) for i in range(2)])
        sums = VGroup(T("Add up the sales:  100 + 104 + 125  =", 26, I.TEXT), TB("$329", 30, I.COST)).arrange(
            RIGHT, buff=0.2).shift(DOWN * 0.5)
        adds = VGroup(T("Add up what each adds:  100 + 4 + 21  =", 26, I.TEXT), TB("$125", 30, I.MONEY),
                      T("the price you paid", 22, I.MONEY)).arrange(RIGHT, buff=0.2).next_to(sums, DOWN, buff=0.4)
        gdp = T("A country's GDP is that second sum, over every firm: the value each one adds.", 22, I.DIM).to_edge(
            DOWN, buff=0.5)
        tag = T("illustrative numbers", 16, I.CHANNEL).to_corner(DR, buff=0.3)
        with self.voiceover(
            "This is the trap from Part one, at the scale of a country. <bookmark mark='a'/> A pill passes from the "
            "drug maker to the wholesaler to the pharmacy, and each one sells it on. <bookmark mark='b'/> Add up "
            "their sales and you count the price of the medicine three times. <bookmark mark='c'/> Add up only what "
            "each one adds, its sales minus what it bought, and you get exactly the price you paid at the counter. "
            "<bookmark mark='d'/> That second sum, taken over every firm in a country, is its gross domestic product. "
            "So the honest way to measure the size of an industry is by its value added, and the rest of this part "
            "uses it."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), LaggedStart(*[GrowArrow(a) for a in
                                                                                             arrows], lag_ratio=0.3),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(sums, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(adds, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(gdp))
        self.clear_scene()
