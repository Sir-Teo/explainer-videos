from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

MEM = "#B58CFF"


class War(VoiceoverScene):
    def construct(self):
        card(self, 10, "Price wars", "Why do industries with huge fixed costs fight to the death?",
             "Chapter ten. Price wars.", lit=("dollar", "who"))
        self.spiral()
        self.micron()
        self.stop()

    # --- the logic of the undercut ------------------------------------------------------------------------------------
    def spiral(self):
        fabs = VGroup()
        for k, (x, nm) in enumerate(((-5.2, "Chipmaker A"), (-2.2, "Chipmaker B"))):
            f = draw.factory(2.0).move_to([x, 1.6, 0])
            w = draw.wafer(0.55, die=0.09).next_to(f, DOWN, buff=0.15)
            fabs.add(VGroup(f, w, tx(nm, 20, MEM, bold=True).next_to(w, DOWN, buff=0.12)))
        ax = CornerAxes(x_range=[0, 9, 1], y_range=[0, 12, 2], x_length=5.6, y_length=4.4,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([3.6, 0.1, 0])
        ac = DashedLine(ax.c2p(0, 7), ax.c2p(9, 7), stroke_color=FIXED, stroke_width=3)
        ac_t = tx("full cost per chip, with the factory", 17, FIXED).next_to(ax.c2p(9, 7), UP, buff=0.06).align_to(
            ax.c2p(9, 7), RIGHT)
        mc = Line(ax.c2p(0, 2), ax.c2p(9, 2), stroke_color=VAR, stroke_width=3)
        mc_t = tx("cost of one more chip", 17, VAR).next_to(ax.c2p(9, 2), DOWN, buff=0.06).align_to(ax.c2p(9, 2), RIGHT)
        prices = [10.0, 8.8, 7.6, 6.4, 5.2, 4.2, 3.4, 2.8, 2.3]
        yl = tx("price of a chip", 18, PRICE).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xl = tx("rounds of undercutting", 18, GREY_B).next_to(ax, DOWN, buff=0.15)
        loss = Rectangle(width=ax.c2p(9, 0)[0] - ax.c2p(5, 0)[0], height=ax.c2p(0, 7)[1] - ax.c2p(0, 2.3)[1],
                         stroke_width=0, fill_color=LOSS, fill_opacity=0.18).move_to(ax.c2p(5, 2.3), aligned_edge=DL)
        loss_t = tx("both lose money\non every chip", 18, LOSS).move_to(loss)
        tag = estimate_tag("illustrative", corner=DR)
        cut = [tx("A cuts", 18, MEM).next_to(fabs[0], UP, buff=0.1), tx("B cuts", 18, MEM).next_to(fabs[1], UP, buff=0.1)]
        with self.voiceover(
            "Put the last few chapters together, and you get the most violent thing in industry: the price war. "
            "<bookmark mark='a'/> Two chipmakers, each with a factory that cost billions. Most of their costs are "
            "fixed: the factory, its machines, its depreciation. The cost of one more chip is a small part of the "
            "total. <bookmark mark='b'/> Demand slips. Each factory has idle capacity, and every chip it can sell "
            "above the cost of one more chip adds to its profit, just like the order in chapter one. "
            "<bookmark mark='c'/> So A cuts its price to win orders. B, losing customers, cuts below A. A cuts "
            "again. <bookmark mark='d'/> There is no natural floor until the price nears the cost of one more chip, "
            "far below what the factories cost. Both are now losing money on every chip, and both keep making them, "
            "because stopping would lose even more."
        ) as vo:
            self.play(FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fabs], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(ac), FadeIn(ac_t), Create(mc), FadeIn(mc_t))
            vo.wait_until("b")
            self.play(*[Rotate(f[1], angle=PI, run_time=2.0) for f in fabs])
            vo.wait_until("c")
            for k in range(4):
                step = VMobject().set_points_as_corners([ax.c2p(k, prices[k]), ax.c2p(k + 1, prices[k]),
                                                         ax.c2p(k + 1, prices[k + 1])]).set_stroke(PRICE, 4)
                self.play(Create(step), FadeIn(cut[k % 2]), run_time=0.7)
                self.play(FadeOut(cut[k % 2]), run_time=0.2)
            vo.wait_until("d")
            rest = VMobject(stroke_color=PRICE, stroke_width=4).set_points_as_corners(
                [p for k in range(4, 9) for p in (ax.c2p(k, prices[k]), ax.c2p(k + 1, prices[k]))])
            self.play(Create(rest), run_time=2.0)
            self.play(FadeIn(loss), FadeIn(loss_t))
        self.clear_scene()

    # --- Micron, 2016-2026 --------------------------------------------------------------------------------------
    def micron(self):
        M = R["memory"]
        yrs = sorted(M["gm"])
        ax = CornerAxes(x_range=[0, 11, 1], y_range=[-0.2, 0.9, 0.1], x_length=10.4, y_length=4.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([0.3, -0.35, 0])
        zero = Line(ax.c2p(0, 0), ax.c2p(11, 0), stroke_color=GREY_B, stroke_width=2)
        bars = VGroup()
        for k, y in enumerate(yrs):
            v = M["gm"][y]
            h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
            b = Rectangle(width=0.62, height=max(h, 0.02), stroke_width=0, fill_color=MEM if v >= 0 else LOSS,
                          fill_opacity=0.9).move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN if v >= 0 else UP)
            lab = tx(f"{100 * v:.0f}%", 17, WHITE if v >= 0 else LOSS, bold=True).next_to(b, UP if v >= 0 else DOWN,
                                                                                          buff=0.06)
            yr = tx(f"{y % 100:02d}", 17, GREY_B).move_to(ax.c2p(k + 0.5, -0.2) + DOWN * 0.3)
            bars.add(VGroup(b, lab, yr))
        head = tx("Micron's gross margin by fiscal year: what is left of each dollar of sales after making the chips",
                  22).to_edge(UP, buff=0.3)
        fy = tx("fiscal year (20..)", 16, GREY_B).next_to(ax, DOWN, buff=0.45)
        src = source("Micron Technology Forms 10-K, FY2016-FY2026 (fiscal years end in late August or early September)")
        i23, i26, i18 = yrs.index(2023), yrs.index(2026), yrs.index(2018)
        wf = draw.wafer(0.7, die=0.1).move_to([-5.2, 2.2, 0])
        with self.voiceover(
            "Memory chips are the textbook case. <bookmark mark='a'/> The chips that hold a computer's working "
            "memory are nearly interchangeable, made in factories that cost tens of billions of dollars, by a few "
            "companies. Here is the American one, Micron: the share of each dollar of sales left after the cost of "
            "making the chips, factory wear included. <bookmark mark='b'/> In the boom of 2018, fifty-nine cents. "
            "<bookmark mark='c'/> Then the makers had built too much, demand for phones and computers sagged, and "
            "prices fell. In fiscal 2023 the margin went below zero: Micron sold its memory for less than it cost "
            "to make. <bookmark mark='d'/> And then the boom in artificial intelligence, which needs vast amounts of "
            "fast memory: in fiscal 2026, eighty-one cents of every dollar. The same company, the same factories, a "
            "swing from minus nine to plus eighty-one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(wf))
            vo.wait_until("a")
            self.play(Create(zero), FadeIn(fy), LaggedStart(*[GrowFromEdge(b[0], DOWN if M["gm"][y] >= 0 else UP)
                                                              for b, y in zip(bars[:3], yrs[:3])], lag_ratio=0.3),
                      *[FadeIn(b[1:]) for b in bars[:3]], run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(bars[i18], color=MEM))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN if M["gm"][y] >= 0 else UP)
                                    for b, y in zip(bars[3:8], yrs[3:8])], lag_ratio=0.3),
                      *[FadeIn(b[1:]) for b in bars[3:8]], run_time=2.5)
            self.play(Indicate(bars[i23], color=LOSS, scale_factor=1.3))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars[8:]], lag_ratio=0.3),
                      *[FadeIn(b[1:]) for b in bars[8:]], run_time=2.5)
            self.play(Indicate(bars[i26], color=PROFIT, scale_factor=1.1))
        self.clear_scene()

    # --- what industries do to stop it ---------------------------------------------------------------------------
    def stop(self):
        M = R["memory"]
        items = [("Collude", "agree prices with rivals:\na crime", f"DRAM makers fined ${1000 * M['fines']:.0f}m\n"
                  "in the US, 2004 to 2006", LOSS, draw.note_bill(0.8, color=LOSS)),
                 ("Merge", "fewer rivals,\nfewer price cuts", f"Micron bought bankrupt\nElpida, {M['elpida']}", FIXED,
                  draw.factory(0.9)),
                 ("Hold back", "build only what\ndemand will buy", "'capacity discipline'", PRICE,
                  draw.wafer(0.35, die=0.07)),
                 ("Be different", "sell what rivals\ncannot make", "memory built\nfor AI chips", PROFIT,
                  draw.chip(0.6))]
        cards = VGroup()
        for name, what, ex, col, glyph in items:
            box = RoundedRectangle(corner_radius=0.15, width=3.1, height=3.6, stroke_color=col, stroke_width=3,
                                   fill_color="#141A24", fill_opacity=1)
            g = glyph.copy()
            g.scale_to_fit_height(0.7)
            body = VGroup(g, tx(name, 32, col, bold=True), tx(what, 20, WHITE), tx(ex, 18, GREY_B)).arrange(DOWN,
                                                                                                             buff=0.28)
            for t_ in body[2:]:
                if t_.width > 2.8:
                    t_.scale_to_fit_width(2.8)
            body.move_to(box)
            cards.add(VGroup(box, body))
        cards.arrange(RIGHT, buff=0.3).move_to([0, -0.2, 0])
        head = tx("Four ways out of a price war", 30, bold=True).to_edge(UP, buff=0.4)
        src = source("US Department of Justice (2005-2006); Micron Form 8-K, 31 July 2013")
        with self.voiceover(
            "Industries like this look for a way out, and there are only four. <bookmark mark='a'/> The first is to "
            "agree prices with your rivals, which is a crime. In the early two-thousands the American government "
            "fined four memory makers a total of more than seven hundred million dollars for fixing the price of "
            "memory chips. <bookmark mark='b'/> The second is to merge, so there are fewer rivals to start a war. "
            "Memory makers went bankrupt or were bought, one after another; Micron bought Japan's Elpida out of "
            "bankruptcy in 2013. <bookmark mark='c'/> The third is discipline: build new capacity only when demand "
            "is there to buy it, and trust your rivals to do the same, which is the phrase you hear on every chip "
            "maker's earnings call. <bookmark mark='d'/> The fourth is to stop selling a commodity: make something "
            "your rivals cannot, as the memory makers now do with the stacked memory that feeds AI chips. "
            "<bookmark mark='e'/> Part five of this series is about exactly this: the moats that let some "
            "industries escape the cost curve's logic, and why so few manage it for long."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark in enumerate("abcd"):
                vo.wait_until(mark)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
            vo.wait_until("e")
            self.play(cards.animate.scale(0.97).set_opacity(0.85))
        self.clear_scene()
