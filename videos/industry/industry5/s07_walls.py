from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Walls(VoiceoverScene):
    def construct(self):
        card(self, 8, "Walls of cost and habit", "What stops a rival from simply copying you?",
             "Chapter eight. Walls of cost and habit.", lit=("moat", "make"))
        self.cost()
        self.habit()

    def cost(self):
        C = R["conc"]
        ax = CornerAxes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=5.4, y_length=3.8,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-3.4, 0.1, 0])
        curve = ax.plot(lambda q: min(9.6, 2.0 + 5.0 / q), x_range=[0.55, 10, 0.02], color="#7EC8F5", stroke_width=4)
        xl = tx("size of the operation", 17, GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = tx("cost per unit", 17, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        big = glow_dot(ax.c2p(8.5, 2.0 + 5.0 / 8.5), color=RET, radius=0.11)
        big_t = tx("the incumbent", 17, RET).next_to(big, UP, buff=0.12)
        small = glow_dot(ax.c2p(1.2, 2.0 + 5.0 / 1.2), color=ENTRANT, radius=0.11)
        small_t = tx("a newcomer", 17, ENTRANT).next_to(small, RIGHT, buff=0.15)
        gap = DoubleArrow(ax.c2p(1.6, 2.0 + 5.0 / 1.2), ax.c2p(1.6, 2.0 + 5.0 / 8.5), buff=0.05, color=GOLD,
                          stroke_width=3, tip_length=0.15)
        gap_t = tx("its cost gap", 16, GOLD).next_to(gap, RIGHT, buff=0.1)
        clubs = C["clubs"]
        card_ = VGroup(tx("Warehouse clubs and supercenters", 22, WHITE, bold=True),
                       tx(f"the four largest: {clubs['cr4']:.0f}% of sales (2022)", 20, GOLD),
                       tx("a newcomer would need the buying power and the", 17, GREY_B),
                       tx("full stores of the largest from its first day", 17, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, 1.3, 0])
        sunk = VGroup(tx("Sunk costs make it worse:", 20, WHITE, bold=True),
                      tx("money a newcomer must risk and cannot get back", 17, GREY_B),
                      tx("if it fails; the incumbent spent it long ago", 17, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, -1.3, 0])
        tag = estimate_tag("the curve is illustrative", corner=DR)
        works = VGroup(draw.factory(0.55, color=ENTRANT).next_to(ax.c2p(1.2, 0), DOWN, buff=0.55),
                       draw.factory(1.3, color=RET).next_to(ax.c2p(8.5, 0), DOWN, buff=0.45))
        src = source("US Census Bureau, 2022 Economic Census: concentration of largest firms", corner=DL)
        with self.voiceover(
            "The first walls are made of cost. <bookmark mark='a'/> Part 4 showed that cost per unit falls with "
            "size and with experience. That is a moat. <bookmark mark='b'/> The incumbent sits at the bottom of the "
            "curve. <bookmark mark='c'/> A newcomer has to start small, at the top, and sell at the incumbent's "
            "price while its own costs are far higher. <bookmark mark='d'/> Warehouse clubs and supercenters are a "
            f"case: the four largest companies had {clubs['cr4']:.0f} percent of the industry's sales in 2022. To "
            "match their prices, a rival would need their buying power and their full stores from its first day. "
            "<bookmark mark='e'/> Sunk costs make the wall higher. A newcomer must risk money it cannot get back if "
            "it fails, while the incumbent spent the same money years ago, as Part 4's chapter on sunk costs "
            "showed."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(src), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(FadeIn(works[0], shift=UP * 0.2), FadeIn(works[1], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Create(curve), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(big, scale=1.5), FadeIn(big_t))
            vo.wait_until("c")
            self.play(FadeIn(small, scale=1.5), FadeIn(small_t))
            self.play(GrowFromCenter(gap), FadeIn(gap_t))
            vo.wait_until("d")
            self.play(FadeIn(card_, shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(sunk, shift=LEFT * 0.2))
        self.clear_scene()

    def habit(self):
        D = {d["name"]: d for d in R["roc"]["industries"]}
        keep = draw.castle(1.8, moat=0.35).move_to([-4.6, 0.6, 0])
        shopper = draw.person(0.8).move_to([-2.2, 0.15, 0])
        rival = draw.castle(1.5, color=ENTRANT).move_to([2.2, 0.6, 0])
        toll = VGroup(Rectangle(width=0.18, height=1.0, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                      Rectangle(width=1.3, height=0.12, stroke_width=0, fill_color=GOLD, fill_opacity=1).shift(
                          UP * 0.35 + RIGHT * 0.55)).move_to([0.0, 0.5, 0])
        toll_t = tx("the cost of switching", 17, GOLD).next_to(toll, UP, buff=0.15)
        kinds = VGroup(tx("a new bank account, new direct debits", 16, GREY_B),
                       tx("retraining staff on new software", 16, GREY_B),
                       tx("a brand you trust without thinking", 16, GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.08).next_to(toll, DOWN,
                                                                                                        buff=0.35)
        brands = VGroup(*[tx(f"{n}: {100 * D[k]['roc']:.0f}%", 20, RET) for n, k in
                          (("soft drinks", "Beverage (Soft)"), ("household products", "Household Products"),
                           ("tobacco", "Tobacco"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        brands_t = tx("returns on capital of brand industries, 2025", 17, GREY_A).next_to(brands, UP, buff=0.15)
        bgroup = VGroup(brands_t, brands).move_to([4.6, -2.3, 0])
        sees = tx("See's, said Buffett, had a 'durable competitive advantage, built by the See's family over a "
                  "50-year period'", 17, "#E9C9A6").to_edge(UP, buff=0.35)
        if sees.width > 13:
            sees.scale_to_fit_width(13)
        src = source("Damodaran, 2025; Berkshire Hathaway letter for 2007", corner=DL)
        with self.voiceover(
            "The second walls are made of habit. <bookmark mark='a'/> A customer can walk across to a rival "
            "whenever she likes. <bookmark mark='b'/> But walking across costs something. Moving a bank account "
            "means new cards and new direct debits; moving a company to new software means retraining everyone; "
            "trying an unknown brand means a risk that the trusted one does not carry. <bookmark mark='c'/> The "
            "rival has to beat the incumbent by more than that toll before anyone moves. <bookmark mark='d'/> "
            "Brands are habit built up over decades. Industries that live on brands, soft drinks, household "
            "products, tobacco, earn some of the highest returns in Damodaran's table. "
            "<bookmark mark='e'/> And that is what Buffett said See's had: a durable advantage, built by the See's "
            "family over fifty years, that no rival could buy in a hurry."
        ) as vo:
            self.play(FadeIn(src), FadeIn(keep, shift=UP * 0.2), FadeIn(shopper))
            vo.wait_until("a")
            self.play(FadeIn(rival, shift=LEFT * 0.2))
            self.play(shopper.animate.shift(RIGHT * 1.4), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(toll, shift=DOWN * 0.2), FadeIn(toll_t), shopper.animate.shift(LEFT * 1.4))
            self.play(LaggedStart(*[FadeIn(k_) for k_ in kinds], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(shopper.animate.shift(RIGHT * 1.6), rate_func=there_and_back, run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(bgroup, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(sees, shift=DOWN * 0.1), Indicate(keep, color="#E9C9A6"))
        self.clear_scene()
