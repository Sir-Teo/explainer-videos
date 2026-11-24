from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Conc(VoiceoverScene):
    def construct(self):
        card(self, 6, "Counting the castles", "How many firms share each market?",
             "Chapter six. Counting the castles.", lit=("moat", "who"))
        self.two_markets()
        self.histogram()

    def two_markets(self):
        C = R["conc"]
        nails, homes = C["nails"], C["homes"]
        # nail salons: a crowd of tiny shops; home centers: four big boxes and a few small ones
        tiny = VGroup(*[draw.shop(0.32, color="#E9A0C9") for _ in range(96)]).arrange_in_grid(rows=8, cols=12,
                                                                                            buff=(0.06, 0.08))
        tiny.move_to([-3.5, -0.2, 0])
        big = VGroup(*[draw.shop(1.35 if k < 2 else 0.95, color="#F2A65A") for k in range(4)])
        big.arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.3)).move_to([3.5, 0.0, 0])
        rest = VGroup(*[draw.shop(0.22, color="#F2A65A") for _ in range(6)]).arrange(RIGHT, buff=0.08).next_to(
            big, DOWN, buff=0.25)
        t1 = VGroup(tx("Nail salons", 26, "#E9A0C9", bold=True),
                    tx(f"{int(nails['firms']):,} firms", 18, GREY_B)).arrange(DOWN, buff=0.06).next_to(tiny, UP, buff=0.3)
        t2 = VGroup(tx("Home centers", 26, "#F2A65A", bold=True),
                    tx(f"{int(homes['firms']):,} firms", 18, GREY_B)).arrange(DOWN, buff=0.06).move_to([3.5, 2.75, 0])
        top1 = tiny[:4].copy()
        cr1 = VGroup(tx("the four largest:", 18, GREY_B), tx(f"{nails['cr4']:.1f}% of sales", 34, WHITE, bold=True)
                     ).arrange(DOWN, buff=0.06).move_to([-3.5, -3.0, 0])
        cr2 = VGroup(tx("the four largest:", 18, GREY_B), tx(f"{homes['cr4']:.0f}% of sales", 34, WHITE, bold=True)
                     ).arrange(DOWN, buff=0.06).move_to([3.5, -3.0, 0])
        src = source("US Census Bureau, 2022 Economic Census: Concentration of Largest Firms (released April 2025)",
                     corner=UL, size=13)
        with self.voiceover(
            "The simplest thing to measure about an industry's castles is how many there are, and how much of the "
            "land the biggest ones hold. Every five years the Census Bureau counts every business in America. "
            "<bookmark mark='a'/> In 2022 it counted thirty-three thousand companies running nail salons. "
            "<bookmark mark='b'/> The four largest together took less than half of one percent of the sales. "
            "<bookmark mark='c'/> It counted under eight hundred companies running home centers, the giant "
            "hardware and building-supply stores. <bookmark mark='d'/> The four largest took ninety-eight percent. "
            "That share, the four largest firms' slice of an industry's sales, is called the four-firm concentration "
            "ratio."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(t1), LaggedStart(*[FadeIn(s_, scale=0.6) for s_ in tiny], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("b")
            self.play(*[s_.animate.set_color(WHITE) for s_ in tiny[:4]], FadeIn(cr1))
            vo.wait_until("c")
            self.play(FadeIn(t2), LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in big], lag_ratio=0.2),
                      FadeIn(rest), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(cr2), Indicate(big, color=WHITE, scale_factor=1.04))
        del top1
        self.clear_scene()

    def histogram(self):
        C = R["conc"]
        hist, edges = C["hist"], C["edges"]
        ax = CornerAxes(x_range=[0, 100, 10], y_range=[0, 190, 50], x_length=8.6, y_length=4.2,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-1.0, -0.4, 0])
        bars = VGroup()
        for k, h in enumerate(hist):
            b = Rectangle(width=ax.c2p(10, 0)[0] - ax.c2p(0, 0)[0] - 0.06, height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=interpolate_color(ManimColor("#7EC8F5"), ManimColor(ENTRANT), k / 9),
                          fill_opacity=0.9).move_to(ax.c2p(edges[k] + 5, 0), aligned_edge=DOWN)
            b.add(tx(f"{h}", 15, GREY_A).next_to(b, UP, buff=0.05))
            bars.add(b)
        xt = VGroup(*[tx(f"{v}%", 15, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0, 25, 50, 75, 100)])
        xl = tx("share of sales held by the four largest firms", 18, GREY_B).next_to(ax, DOWN, buff=0.45)
        yl = tx("number of industries", 18, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        med = DashedLine(ax.c2p(C["median"], 0), ax.c2p(C["median"], 185), stroke_color=WHITE, stroke_width=2)
        med_t = tx(f"median {C['median']:.0f}%", 17, WHITE).next_to(ax.c2p(C["median"], 185), UP, buff=0.05)
        top = VGroup(*[tx(f"{d['name'][:38]}  {d['cr4']:.0f}%", 15, ENTRANT) for d in reversed(C["high"][-8:])])
        top.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.0, 0.3, 0])
        top_t = tx("among the most concentrated", 17, GREY_A, bold=True).next_to(top, UP, buff=0.2).align_to(top, LEFT)
        warn = tx("A national share can mislead: one town's only hospital, or two airlines at one airport, are "
                  "local monopolies in a 'competitive' industry.", 17, GOLD).to_edge(DOWN, buff=0.15)
        if warn.width > 13:
            warn.scale_to_fit_width(13)
        src = source("US Census Bureau, 2022 Economic Census; 897 six-digit industries with a published ratio",
                     corner=UL, size=13)
        with self.voiceover(
            f"Do that for all {C['n']} industries the Census reports, and you get this. <bookmark mark='a'/> Most "
            f"American industries are not very concentrated: in the median industry the four largest firms hold "
            f"about {C['median']:.0f} percent of sales, and in more than a quarter of industries they hold less than "
            f"twenty. <bookmark mark='b'/> The long tail on the right is the castles: warehouse clubs, wireless "
            "carriers, tobacco, breakfast cereal, web search, kidney dialysis, where four firms or fewer hold most "
            "of the market. <bookmark mark='c'/> A warning before using these numbers. A market is where buyers can "
            "actually choose between sellers, and that is often smaller than a national industry: a town's only "
            "hospital is a monopoly whatever the national figure says. Antitrust lawyers spend careers arguing "
            "about exactly where a market's edges are."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(src))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(med), FadeIn(med_t))
            vo.wait_until("b")
            self.play(FadeIn(top_t), LaggedStart(*[FadeIn(t_, shift=LEFT * 0.1) for t_ in top], lag_ratio=0.1),
                      Indicate(VGroup(*bars[7:]), color=ENTRANT), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(warn, shift=UP * 0.1))
        self.clear_scene()
