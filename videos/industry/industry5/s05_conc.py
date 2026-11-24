from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Conc(VoiceoverScene):
    def construct(self):
        card(self, 6, "Counting the castles", "How many firms share each market?",
             "Chapter six. Counting the castles.", lit=("moat", "who"))
        self.two_markets()
        self.histogram()
        self.hhi()

    def hhi(self):
        from explainer.industry.register import get
        markets = [("four equal firms", [25] * 4), ("one big firm and three small ones", [55, 15, 15, 15]),
                   ("twenty equal firms", [5] * 20)]
        groups = VGroup()
        for name, shares in markets:
            # each firm is a square as wide as its share, so its area is its share squared
            sq = VGroup(*[Square(0.042 * s + 0.03, stroke_width=1, stroke_color="#0E1117", fill_color=ENTRANT,
                                 fill_opacity=0.85) for s in shares])
            sq.arrange_in_grid(cols=min(len(shares), 5), buff=0.06, aligned_edge=DOWN)
            val = sum(s * s for s in shares)
            label = VGroup(tx(name, 18, GREY_A), tx(f"HHI = {val:,}", 26, WHITE, bold=True)).arrange(DOWN, buff=0.08)
            groups.add(VGroup(sq, label.next_to(sq, DOWN, buff=0.25)))
        groups.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to([0, -0.2, 0])
        eq = MathTex(r"\text{HHI} = s_1^2 + s_2^2 + \dots + s_n^2", font_size=40).to_edge(UP, buff=0.5)
        line = tx(f"the US merger guidelines (2023): above {int(get('hhi.2023')):,}, a market is 'highly "
                  "concentrated'", 20, GOLD).to_edge(DOWN, buff=0.45)
        src = source("US Department of Justice and FTC, Merger Guidelines (2023), Guideline 1", corner=DR)
        # the four-firm ratio cannot tell these two markets apart
        splits = VGroup()
        for shares in ([25] * 4, [55, 15, 15, 15]):
            bar = VGroup(*[Rectangle(width=0.08 * s_, height=0.55, stroke_color="#0E1117", stroke_width=3,
                                     fill_color=ENTRANT, fill_opacity=0.85) for s_ in shares]).arrange(RIGHT, buff=0)
            lab = VGroup(*[tx(f"{s_}%", 16, WHITE).move_to(b_) for s_, b_ in zip(shares, bar)])
            splits.add(VGroup(bar, lab, tx("four largest: 100%", 18, GREY_A).next_to(bar, RIGHT, buff=0.3)))
        splits.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, 0.2, 0])
        with self.voiceover(
            "The four-firm ratio ignores how the share is split. Regulators use a second measure, named after "
            "the economists Orris Herfindahl and Albert Hirschman. <bookmark mark='a'/> Square each firm's share of "
            "the market, in percent, and add them up. <bookmark mark='b'/> Four equal firms with a quarter each give "
            "two thousand five hundred. <bookmark mark='c'/> If one of them has fifty-five percent and the others "
            "fifteen each, the total jumps to nearly four thousand, because squaring makes the big firm count for "
            "much more. <bookmark mark='d'/> Twenty equal firms give five hundred. <bookmark mark='e'/> American "
            "competition authorities treat a market above one thousand eight hundred as highly concentrated, and "
            "look hard at any merger that pushes it there, or adds more than a hundred points to a market already "
            "above it."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(sp_, shift=RIGHT * 0.2) for sp_ in splits], lag_ratio=0.5),
                      run_time=1.6)
            vo.wait_until("a")
            self.play(FadeOut(splits), Write(eq))
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(LaggedStart(*[GrowFromCenter(s_) for s_ in groups[k][0]], lag_ratio=0.03),
                          FadeIn(groups[k][1]), run_time=1.4)
            vo.wait_until("e")
            self.play(FadeIn(line, shift=UP * 0.1))
        self.clear_scene()

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
            for m_ in (tiny, big, rest):
                m_.set_opacity(0.22)
            self.play(FadeIn(src), LaggedStart(*[FadeIn(s_, scale=0.6) for s_ in tiny], lag_ratio=0.005),
                      LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in big], lag_ratio=0.2), FadeIn(rest),
                      run_time=2.4)
            vo.wait_until("a")
            self.play(FadeIn(t1), LaggedStart(*[s_.animate.set_opacity(1) for s_ in tiny], lag_ratio=0.01),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(*[s_.animate.set_color(WHITE) for s_ in tiny[:4]], FadeIn(cr1))
            vo.wait_until("c")
            self.play(FadeIn(t2), LaggedStart(*[s_.animate.set_opacity(1) for s_ in big], lag_ratio=0.2),
                      rest.animate.set_opacity(1), run_time=1.8)
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
