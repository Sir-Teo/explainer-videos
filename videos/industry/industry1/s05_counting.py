from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403


class Counting(VoiceoverScene):
    def construct(self):
        card(self, 4, "Counting the money once", "Why can't we just add up everyone's sales?",
             "Chapter four. Counting the money once.", lit=("dollar",))
        self.chain()
        self.added()

    def chain(self):
        A = R["added"]["chain"]
        colors = (I.OTHER, I.CHIP, I.BRAND, I.CHANNEL)
        boxes = VGroup()
        for link, c in zip(A, colors):
            box = RoundedRectangle(corner_radius=0.14, width=2.75, height=1.5, fill_color=c, fill_opacity=0.14,
                                   stroke_color=c, stroke_width=2.2)
            body = VGroup(T(link["firm"], 20, I.TEXT), T("sells for", 17, I.DIM), TB(money(link["sales"]), 32, c)
                          ).arrange(DOWN, buff=0.08).move_to(box)
            boxes.add(VGroup(box, body))
        boxes.arrange(RIGHT, buff=0.55).shift(UP * 1.6)
        arrows = VGroup(*[viz.arrow_line(boxes[i].get_right(), boxes[i + 1].get_left()) for i in range(3)])
        goods = T("goods flow this way  →", 18, I.DIM).next_to(arrows, UP, buff=1.85)
        glyphs = VGroup(draw.wafer(0.32, die=0.06), draw.chip(0.55, color=I.CHIP),
                        viz.phone(0.75, back=True, body=BODY_17), draw.shop(0.8, color=I.CHANNEL))
        for g_, b in zip(glyphs, boxes):
            g_.next_to(b, UP, buff=0.18)
        token = draw.wafer(0.2, die=0.05).move_to(boxes[0].get_top() + UP * 0.05)
        cust = VGroup(T("You pay", 20, I.DIM), TB(money(R["dollar17"]["price"]), 26, I.MONEY)).arrange(
            DOWN, buff=0.05).next_to(boxes[-1], DOWN, buff=0.3)
        coins = VGroup(*[viz.coin(0.12) for _ in range(4)])
        # the sales, stacked: the same money counted at every link
        L = 11.0
        scale = L / R["added"]["sales_total"]
        stack = VGroup()
        for link, c in zip(A, colors):
            stack.add(Rectangle(width=max(scale * link["sales"], 0.03), height=0.55, fill_color=c, fill_opacity=0.85,
                                stroke_color="#0E1117", stroke_width=1.2))
        stack.arrange(RIGHT, buff=0).move_to(DOWN * 1.1)
        price = Rectangle(width=scale * R["dollar17"]["price"], height=0.55, stroke_color=I.MONEY, stroke_width=2.5,
                          fill_opacity=0).align_to(stack, LEFT).shift(DOWN * 2.0)
        lab_s = VGroup(T("Add up everyone's sales:", 22, I.TEXT), TB(money(R["added"]["sales_total"]), 28, I.COST)
                       ).arrange(RIGHT, buff=0.2).next_to(stack, UP, buff=0.15).align_to(stack, LEFT)
        lab_p = VGroup(T("what you actually paid:", 22, I.TEXT), TB(money(R["dollar17"]["price"]), 28, I.MONEY)
                       ).arrange(RIGHT, buff=0.2).next_to(price, RIGHT, buff=0.25)
        tag = T("a simplified chain: as if Apple bought only the chip", 17, I.DIM).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Before we follow the 1,099 dollars, a trap to avoid. <bookmark mark='a'/> Picture the chain as four "
            "firms. A supplier sells silicon wafers and materials, for about 10 dollars per phone. TSMC turns them "
            "into a processor and sells it to Apple for about 83. Apple sells the finished phone to a carrier for "
            "about 1,033. The carrier sells it to you for 1,099. <bookmark mark='b'/> The money flows the other "
            "way: from you, to the shop, to Apple, to TSMC, to the wafer maker. <bookmark mark='c'/> Now add up "
            "everyone's sales. You get more than 2,200 dollars, for a phone that cost 1,099. <bookmark mark='d'/> "
            "The total is wrong because each firm's sales include everything it bought from the firm before it. "
            "The chip's 83 dollars is counted once in TSMC's sales, again inside Apple's, and a third time inside "
            "the shop's."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in boxes], lag_ratio=0.35),
                      LaggedStart(*[FadeIn(g_, shift=DOWN * 0.15) for g_ in glyphs], lag_ratio=0.35),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.35), run_time=2.6)
            self.play(FadeIn(goods), FadeIn(cust), FadeIn(token, scale=0.5))
            # the thing being made travels down the chain, changing as it goes
            for i in range(3):
                nxt = glyphs[i + 1].copy().scale_to_fit_height(0.45)
                self.play(token.animate.move_to(arrows[i].get_center() + UP * 0.35), run_time=0.6)
                self.play(Transform(token, nxt.move_to(arrows[i].get_center() + UP * 0.35)), run_time=0.4)
            self.play(token.animate.move_to(cust.get_bottom() + DOWN * 0.35), run_time=0.7)
            vo.wait_until("b")
            for i, c in enumerate(coins):
                c.move_to(cust)
                self.add(c)
            self.play(*[c.animate.move_to(boxes[3 - i].get_bottom() + DOWN * 0.15) for i, c in enumerate(coins)],
                      run_time=1.2)
            self.play(LaggedStart(*[c.animate.move_to(boxes[max(2 - i, 0)].get_center()) for i, c in enumerate(coins)],
                                  lag_ratio=0.2), run_time=1.6)
            self.play(FadeOut(coins), FadeOut(token))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in stack], lag_ratio=0.25), FadeIn(lab_s),
                      run_time=1.8)
            self.play(Create(price), FadeIn(lab_p))
            vo.wait_until("d")
            self.play(Indicate(stack[1], color=I.CHIP, scale_factor=1.3))
        self.keep = VGroup(boxes, arrows, goods, cust, tag, glyphs)
        self.play(FadeOut(VGroup(stack, price, lab_s, lab_p)))

    def added(self):
        A = R["added"]["chain"]
        colors = (I.OTHER, I.CHIP, I.BRAND, I.CHANNEL)
        L = 11.0
        scale = L / R["dollar17"]["price"]
        bars = VGroup(*[Rectangle(width=max(scale * a["added"], 0.04), height=0.65, fill_color=c, fill_opacity=0.9,
                                  stroke_color="#0E1117", stroke_width=1.2) for a, c in zip(A, colors)])
        bars.arrange(RIGHT, buff=0).move_to(DOWN * 1.3)
        frame_ = Rectangle(width=L, height=0.65, stroke_color=I.MONEY, stroke_width=2.5).move_to(bars)
        labs = VGroup()
        for a, b, c in zip(A, bars, colors):
            lab = VGroup(TB(money(a["added"]), 22, c), T(a["firm"].split(":")[0], 15, I.DIM)).arrange(DOWN, buff=0.04)
            labs.add(lab.next_to(b, DOWN, buff=0.15))
        labs[0].next_to(bars[0], UP, buff=0.15).shift(LEFT * 0.2)
        labs[1].shift(RIGHT * 0.25)
        eq = VGroup(T("value added  =  your sales  -  what you bought from others", 24, I.TEXT)).next_to(
            frame_, UP, buff=0.75)
        total = VGroup(T("Add up value added:", 22, I.TEXT), TB(money(R["dollar17"]["price"]), 28, I.MONEY),
                       T("exactly the price", 22, I.MONEY)).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.45)
        gdp = T("Gross domestic product is the same sum, over every firm in a country", 20, I.DIM).next_to(
            total, UP, buff=0.12)
        with self.voiceover(
            "The fix is to count what each firm adds. <bookmark mark='a'/> Value added is a firm's sales minus what "
            "it bought from other firms. <bookmark mark='b'/> The wafer maker adds 10 dollars; TSMC adds 73; Apple "
            "adds about 950; the shop adds 66. <bookmark mark='c'/> These add up to exactly the price you paid, not "
            "a cent more. This is how statistical offices measure an economy's output: a country's gross domestic "
            "product is the sum of the value added by every firm in it. <bookmark mark='d'/> Two warnings. Apple's "
            "950 dollars here still contains every other part it bought, the display, the memory, the cameras, "
            "because this little chain pretends Apple bought only a chip. And value added is not profit: it pays "
            "the firm's workers and its machines as well as its owners. In the next chapter we split Apple's share "
            "into those pieces."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(eq), Create(frame_))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(l)) for b, l in zip(bars, labs)],
                                  lag_ratio=0.4), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(total, shift=UP * 0.1), FadeIn(gdp))
            vo.wait_until("d")
            self.play(Indicate(bars[2], color=I.BRAND, scale_factor=1.08))
        self.clear_scene()
