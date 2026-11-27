from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Minimills(VoiceoverScene):
    def construct(self):
        card(self, 5, "Disruption from below", "How did small scrap-melting mills take over American steel?",
             "Chapter five. Disruption from below.", lit=("moat", "change"))
        self.ladder()
        self.share()
        self.duel()

    def ladder(self):
        M = R["minimills"]
        steps = [("rebar", "the bars inside concrete", draw.rebar(1.0, 4)), ("bars and angles", "for frames and machines",
                                                                           draw.rebar(1.0, 2, "#8B95A7")),
                 ("structural beams", "for buildings and bridges", draw.ibeam(0.5)),
                 ("sheet", "for cars and appliances: the best margins", draw.coil(0.3))]
        stair = VGroup()
        for i, (n, d, ic) in enumerate(steps):
            x, y = -4.6 + 2.6 * i, -2.6 + 1.05 * i
            blk = Rectangle(width=2.5, height=0.5, stroke_width=0, fill_color=ORE, fill_opacity=0.75).move_to([x, y, 0])
            ic.scale_to_fit_height(0.45)
            if ic.width > 1.2:
                ic.scale_to_fit_width(1.2)
            ic.next_to(blk, UP, buff=0.1)
            lab = VGroup(tx(n, 17, WHITE, bold=True), tx(d, 12, GREY_A)).arrange(DOWN, buff=0.02).move_to(blk)
            stair.add(VGroup(blk, ic, lab))
        axis = Arrow([-6.4, -3.1, 0], [-6.4, 2.2, 0], buff=0, color=GREY_B, stroke_width=2, tip_length=0.15)
        al = tx("quality and margin", 14, GREY_B).rotate(PI / 2).next_to(axis, RIGHT, buff=0.1)
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=ORE, fill_opacity=0.75), tx("integrated mills", 14, ORE)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=SCRAP, fill_opacity=0.9), tx("minimills", 14, SCRAP)
                            ).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UR, buff=0.5)
        dates = [tx(f"{M['darlington']:.0f}: Nucor's first mini mill, Darlington, South Carolina", 15, SCRAP),
                 tx("the 1970s and 1980s: bars, angles, small shapes", 14, SCRAP),
                 tx("1988: Nucor-Yamato, wide-flange beams", 14, SCRAP),
                 tx("end of the 1980s: thin slabs at Crawfordsville, Indiana", 14, SCRAP)]
        for d_, st in zip(dates, stair):
            d_.next_to(st[0], DOWN, buff=0.1)
        src = source("Nucor Corporation, 'History'; Clayton Christensen, The Innovator's Dilemma (1997)", size=13)
        with self.voiceover(
            "The minimill is the most famous story in business schools of an industry overturned from below. The "
            "Harvard professor Clayton Christensen made it his textbook case. <bookmark mark='a'/> Steel products form "
            "a ladder, from the cheapest, rebar, the ribbed bars buried in concrete, up through bars and angles, "
            "structural beams, and at the top, the flat sheet that goes into cars and refrigerators, where the margins "
            "were best. In the 1960s the big integrated mills made all of it. <bookmark mark='b'/> The first minimills "
            "could only make the bottom rung. Their scrap steel was not good enough for anything else. Nucor's first, "
            "at Darlington in South Carolina, started in 1969 to supply the company's own joist plants. The integrated "
            "mills were glad to give rebar up: its margins were thin. <bookmark mark='c'/> Then the minimills got better, "
            "and climbed: bars and angles in the seventies and eighties, <bookmark mark='d'/> beams, when Nucor and "
            "Japan's Yamato Kogyo built a beam mill in Arkansas in 1988, <bookmark mark='e'/> and finally sheet, when "
            "at the end of the 1980s Nucor's mill at Crawfordsville, Indiana, became the first minimill in the world to "
            "make quality flat-rolled steel by casting thin slabs. At every step, the integrated mills retreated upward, "
            "to the business that was left, until there was little left to retreat to."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(al), FadeIn(key), FadeIn(src),
                      LaggedStart(*[FadeIn(s_, shift=UP * 0.15) for s_ in stair], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(s_[2], color=PRICE, scale_factor=1.1) for s_ in stair], lag_ratio=0.3),
                      run_time=2.0)
            for m_, k in zip("bcde", range(4)):
                vo.wait_until(m_)
                self.play(stair[k][0].animate.set_fill(SCRAP, 0.9), FadeIn(dates[k], shift=UP * 0.1), run_time=1.0)
        self.clear_scene()

    def share(self):
        M = R["minimills"]
        e = M["eaf_share"]
        ys = sorted(e)
        bars = VGroup()
        for i, y in enumerate(ys):
            h = 4.0 * e[y] / 100
            b = Rectangle(width=1.3, height=h, stroke_width=0, fill_color=SCRAP, fill_opacity=0.9).move_to(
                [-3.6 + 2.4 * i, -2.5, 0], aligned_edge=DOWN)
            bg = Rectangle(width=1.3, height=4.0, stroke_width=0, fill_color=ORE, fill_opacity=0.35).move_to(
                [-3.6 + 2.4 * i, -2.5, 0], aligned_edge=DOWN)
            bars.add(VGroup(bg, b, tx(f"{e[y]:.0f}%", 22, WHITE, bold=True).next_to(b, UP, buff=0.08),
                            tx(str(y), 18, GREY_A).next_to(bg, DOWN, buff=0.1)))
        head = tx("Share of US steel made in electric furnaces", 24, WHITE, bold=True).to_edge(UP, buff=0.5)
        src = source("World Steel Association: Steel Statistical Yearbooks 2002 and 2020; World Steel in Figures 2026", size=13)
        with self.voiceover(
            "Here is the result in one series: the share of American steel made in electric furnaces. "
            f"<bookmark mark='a'/> {e[1992]:.0f} per cent in 1992. <bookmark mark='b'/> {e[2000]:.0f} per cent in 2000. "
            f"<bookmark mark='c'/> {e[2019]:.0f} per cent in 2019. <bookmark mark='d'/> And {e[2025]:.0f} per cent in "
            "2025. The blast furnace, which made almost all of America's steel for a century, now makes less than a "
            "third of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(VGroup(b[0], b[3])) for b in bars])
            for m_, b in zip("abcd", bars):
                vo.wait_until(m_)
                self.play(GrowFromEdge(b[1], DOWN), FadeIn(b[2]), run_time=1.0)
        self.clear_scene()

    def duel(self):
        M = R["minimills"]
        rev = M["revenue"]
        ys = list(range(2010, 2025))
        pa = viz.plot_axes([2009.5, 2025.5], [0, 45], x_length=7.2, y_length=4.2, xticks=[2010, 2015, 2020, 2024],
                           yticks=[10, 20, 30, 40], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="revenue", size=13).move_to([-2.4, -0.3, 0])
        ln = VMobject(stroke_color=SCRAP, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, rev["NUE"][y]) for y in ys])
        lx = VMobject(stroke_color=ORE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, rev["X"][y]) for y in ys])
        tn = tx("Nucor", 16, SCRAP, bold=True).next_to(pa.ax.c2p(2024, rev["NUE"][2024]), RIGHT, buff=0.1)
        tx_ = tx("US Steel", 16, ORE, bold=True).next_to(pa.ax.c2p(2024, rev["X"][2024]), RIGHT, buff=0.1)
        c = M["cum_net"]
        cum = VGroup(tx("Profit, 2010-2024, added up", 18, WHITE, bold=True),
                     VGroup(tx("Nucor", 18, SCRAP, bold=True), tx(f"${c['NUE']:.0f} billion", 26, SCRAP, bold=True)).arrange(
                         RIGHT, buff=0.3),
                     VGroup(tx("US Steel", 18, ORE, bold=True), tx(f"${c['X']:.0f} billion", 26, ORE, bold=True)).arrange(
                         RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, 0.6, 0])
        head = tx("Two American steelmakers", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        end = VGroup(tx("June 2025: US Steel is bought by", 16, GREY_A), tx("Japan's Nippon Steel", 18, WHITE, bold=True)
                     ).arrange(DOWN, buff=0.04).next_to(cum, DOWN, buff=0.5)
        src = source("SEC company facts, Forms 10-K (revenue; net income attributable to the company); USGS, Mineral "
                     "Commodity Summaries 2026", size=13)
        with self.voiceover(
            "And here it is in two companies. <bookmark mark='a'/> In 2010, Nucor and US Steel, a corporation "
            "established in 1901, the giant of American steel for most of the century since, had about the same "
            "revenue. "
            "<bookmark mark='b'/> By 2024, Nucor's was twice US Steel's. <bookmark mark='c'/> Add up the profits from 2010 "
            f"to 2024: Nucor, about {c['NUE']:.0f} billion dollars. US Steel, about {c['X']:.0f} billion. "
            "<bookmark mark='d'/> In June 2025, US Steel was bought by Japan's Nippon Steel, with the American "
            "government's approval and conditions."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(Dot(pa.ax.c2p(2010, rev["NUE"][2010]), color=SCRAP)),
                      FadeIn(Dot(pa.ax.c2p(2010, rev["X"][2010]), color=ORE)))
            vo.wait_until("b")
            self.play(Create(ln), Create(lx), run_time=3.0, rate_func=linear)
            self.play(FadeIn(tn), FadeIn(tx_))
            vo.wait_until("c")
            self.play(FadeIn(cum, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
