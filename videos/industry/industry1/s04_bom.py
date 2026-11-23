from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403

PARTS_ORDER = ("display", "chip", "camera", "rf", "memory", "case", "power", "other")


class Bom(VoiceoverScene):
    def construct(self):
        card(self, 3, "What the parts cost", "What does a teardown see, and what does it miss?",
             "Chapter three. What the parts cost.", lit=("make",))
        self.teardown()
        self.gap()
        self.unseen()

    def teardown(self):
        D = R["dollar17"]
        parts = [s for s in D["slices"] if s["group"] == "parts"]
        lo, hi = 450, 570
        tiles = VGroup()
        for s in parts:
            c = COL[s["key"]]
            box = RoundedRectangle(corner_radius=0.12, width=3.05, height=1.35, fill_color=c, fill_opacity=0.14,
                                   stroke_color=c, stroke_width=2)
            body = VGroup(TB(money(s["amount"]), 30, c), T(s["label"], 19, I.TEXT), T(s["who"], 14, I.DIM)
                          ).arrange(DOWN, buff=0.07)
            if body.width > 2.85:
                body.scale_to_fit_width(2.85)
            tiles.add(VGroup(box, body.move_to(box)))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.25)).shift(UP * 0.55)
        total = VGroup(T("All the parts:", 28, I.TEXT), TB(money(D["bom"]), 40, I.MONEY),
                       T(f"(published estimates range from {money(lo)} to {money(hi)})", 22, I.DIM)
                       ).arrange(RIGHT, buff=0.25).next_to(tiles, DOWN, buff=0.5)
        tag = estimate_tag("estimate: the split is this film's")
        src = source("TrendForce, WSJ via MacRumors (2026); teardown houses' published splits")
        with self.voiceover(
            "There are companies whose business is taking phones apart. They buy one on launch day, strip it down to "
            "the chips, identify every part and estimate what each one costs. <bookmark mark='a'/> Their full "
            "estimates for this phone are sold to clients, but the figures that have been reported put the parts of "
            "a 256-gigabyte iPhone 17 Pro at roughly 450 to 570 dollars. We will use 520. <bookmark mark='b'/> Split "
            "it the way teardowns do. The display and the processor are the two biggest lines, at about 80 to 90 "
            "dollars each. The cameras come next, then the modem and the radios. <bookmark mark='c'/> Memory and "
            "storage come to about 52 dollars, a tenth of the bill. Remember that number. <bookmark mark='d'/> Then "
            "the frame and glass, the battery, and a long tail of small parts: speakers, the vibration motor, "
            "sensors, the circuit board itself."
        ) as vo:
            ph = viz.phone(3.6, back=True, body=BODY_17).move_to(ORIGIN + UP * 0.2)
            tools = VGroup(Line(LEFT * 0.5, RIGHT * 0.5, stroke_color="#C9D3E0", stroke_width=5),
                           RoundedRectangle(corner_radius=0.05, width=0.35, height=0.16, stroke_width=0,
                                            fill_color="#E8554E", fill_opacity=1).shift(LEFT * 0.6)).rotate(-0.6)
            tools.next_to(ph, RIGHT, buff=0.3)
            self.play(FadeIn(src), FadeIn(tag), FadeIn(ph, shift=UP * 0.2), FadeIn(tools, shift=LEFT * 0.2))
            self.play(tools.animate.shift(LEFT * 0.25 + DOWN * 0.15), rate_func=there_and_back, run_time=0.8)

            def pull(i):
                chip_ = draw.chip(0.45, color=COL[parts[i]["key"]]).move_to(ph.get_center())
                return chip_, AnimationGroup(chip_.animate.move_to(tiles[i].get_center()).scale(0.4).set_opacity(0),
                                             FadeIn(tiles[i], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(ph.animate.scale(0.33).move_to(UP * 2.95), FadeOut(tools),
                      FadeIn(total[0]), FadeIn(total[1]), FadeIn(total[2]))
            vo.wait_until("b")
            pulls = [pull(i) for i in range(4)]
            self.add(*[c for c, _ in pulls])
            self.play(LaggedStart(*[a_ for _, a_ in pulls], lag_ratio=0.3), run_time=2.2)
            self.remove(*[c for c, _ in pulls])
            vo.wait_until("c")
            c4, a4 = pull(4)
            self.add(c4)
            self.play(a4)
            self.remove(c4)
            self.play(Indicate(tiles[4], color=I.MEMORY, scale_factor=1.08))
            vo.wait_until("d")
            pulls = [pull(i) for i in range(5, len(tiles))]
            self.add(*[c for c, _ in pulls])
            self.play(LaggedStart(*[a_ for _, a_ in pulls], lag_ratio=0.3), run_time=1.8)
            self.remove(*[c for c, _ in pulls])
        self.clear_scene()

    def gap(self):
        D = R["dollar17"]
        price, bom = D["price"], D["bom"]
        marginal = bom + amount("assembly") + amount("other_cogs")
        L = 11.0
        top = Rectangle(width=L, height=0.8, fill_color=I.MONEY, fill_opacity=0.25, stroke_color=I.MONEY,
                        stroke_width=2).shift(UP * 1.2)
        partsbar = Rectangle(width=L * bom / price, height=0.8, fill_color=COL["parts"], fill_opacity=0.9,
                             stroke_width=0).align_to(top, LEFT).shift(DOWN * 0.0).set_y(-0.2)
        extra = Rectangle(width=L * (marginal - bom) / price, height=0.8, fill_color=I.ASSEMBLY, fill_opacity=0.9,
                          stroke_width=0).next_to(partsbar, RIGHT, buff=0)
        l1 = VGroup(TB(money(price), 28, I.MONEY), T("the price", 22, I.TEXT)).arrange(RIGHT, buff=0.2
                    ).next_to(top, UP, buff=0.15).align_to(top, LEFT)
        l2 = VGroup(TB(money(bom), 28, COL["parts"]), T("the parts", 22, I.TEXT)).arrange(RIGHT, buff=0.2
                    ).next_to(partsbar, DOWN, buff=0.15).align_to(partsbar, LEFT)
        l3 = VGroup(TB(f"+ {money(marginal - bom)}", 26, I.ASSEMBLY), T("assembly, shipping, warranty", 20, I.DIM)
                    ).arrange(RIGHT, buff=0.15).next_to(extra, DOWN, buff=0.15).align_to(extra, LEFT).shift(DOWN * 0.45)
        one_more = VGroup(T("What one more phone costs Apple: about", 26, I.TEXT), TB(money(marginal), 34, I.TEXT)
                          ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=1.2)
        fixed = VGroup(T("What it costs to design the next one is not in that figure:", 22, I.DIM),
                       T(f"Apple spent {money_short(45.765)} on research and development in fiscal 2026", 22,
                         I.BRAND)).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.35)
        src = source("Apple Form 10-K FY2026 (R&D $45,765m)", corner=UR)
        with self.voiceover(
            "Put the parts next to the price. <bookmark mark='a'/> 520 dollars of parts in a 1,099-dollar phone: "
            "less than half. <bookmark mark='b'/> Add assembly, shipping, the warranty and the licences paid on each "
            "phone, and what it costs Apple to make one more is about 590 dollars. <bookmark mark='c'/> It is "
            "tempting to read the rest, about 500 dollars, as profit. It is not, and the reason is the most "
            "important idea in this chapter: one more phone is cheap, but the first one is not. <bookmark "
            "mark='d'/> Before a single phone is sold, someone has to design the chip, write the software, and run "
            "the stores and the advertising. In its last fiscal year Apple spent 45.8 billion dollars on research "
            "and development alone. Those costs do not grow with each phone; they are spread over every phone sold."
        ) as vo:
            self.play(FadeIn(top), FadeIn(l1), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(partsbar, LEFT), FadeIn(l2), run_time=1.4)
            vo.wait_until("b")
            self.play(GrowFromEdge(extra, LEFT), FadeIn(l3))
            self.play(FadeIn(one_more, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(fixed, shift=UP * 0.1))
        self.clear_scene()

    def unseen(self):
        seen = VGroup(TB("A teardown sees", 28, I.TEXT), T("chips, glass, metal, batteries", 24, I.DIM),
                      T("and estimates their factory price", 24, I.DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        unseen = VGroup(TB("It cannot see", 28, I.ACCENT))
        for t in ("years of engineering behind each part", "the software on it", "the patents it licenses",
                  "the brand, the advertising, the stores", "the support after the sale"):
            unseen.add(T("·  " + t, 24, I.TEXT))
        unseen.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        g = VGroup(seen, unseen).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(UP * 0.2)
        line = T("A part's price is what its maker could charge, not what it is worth to the phone.", 24, I.MONEY
                 ).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So a teardown answers part of the question. <bookmark mark='a'/> It sees atoms: chips, glass, metal, "
            "batteries, and what their makers charge for them. <bookmark mark='b'/> It cannot see the years of "
            "engineering behind each part, the software, the patents licensed on every phone, the brand, the "
            "stores, or the support after the sale. <bookmark mark='c'/> And it tells us what each maker could "
            "charge, which is not the same as what its part is worth. That difference, between what a link "
            "contributes and what it can charge, is where this whole part is heading."
        ) as vo:
            self.play(FadeIn(seen[0]))
            vo.wait_until("a")
            self.play(FadeIn(seen[1:], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in unseen], lag_ratio=0.25), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(line, shift=UP * 0.1))
        self.clear_scene()
