from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.payment()
        self.real()
        self.newprice()
        self.three()
        self.title()

    def payment(self):
        H = R["hook"]
        a, b = H["m21"], H["m26"]
        houses = VGroup(draw.house(1.6), draw.house(1.6, color="#F2D0A4")).arrange(RIGHT, buff=4.6).move_to([0, 1.7, 0])
        left = VGroup(tx("January 2021", 18, GREY_A), tx(f"median new house {money(H['price'][a])}", 17, WHITE),
                      tx(f"30-year mortgage at {H['rate'][a]:.2f}%", 17, LOAN),
                      tx(f"{money(H['pay'][a])} a month", 30, GOOD, bold=True)).arrange(DOWN, buff=0.15).move_to([-3.4, -0.9, 0])
        right = VGroup(tx("October 2026", 18, GREY_A), tx(f"median new house {money(H['price'][b])}", 17, WHITE),
                       tx(f"30-year mortgage at {H['rate'][b]:.2f}%", 17, LOAN),
                       tx(f"{money(H['pay'][b])} a month", 30, BAD, bold=True)).arrange(DOWN, buff=0.15).move_to([3.4, -0.9, 0])
        tag = estimate_tag("this series' arithmetic: 10% down, principal and interest only", size=12)
        src = source("Census and HUD, median sales price of new houses sold; Freddie Mac, 30-year fixed rate (monthly "
                     "averages), via FRED", size=12)
        up = 100 * (H["pay"][b] / H["pay"][a] - 1)
        beat(self,
             "Two Americans buy the same kind of new house, five years apart. <bookmark mark='a'/> In January 2021 the "
             f"median new house sold for {H['price'][a]:,.0f} dollars, and a thirty-year mortgage cost {H['rate'][a]:.1f} per "
             f"cent. With ten per cent down, the monthly payment was about {H['pay'][a]:,.0f} dollars. "
             f"<bookmark mark='b'/> In October 2026 the median new house sold for {H['price'][b]:,.0f}, only a little more, "
             f"but the mortgage rate was {H['rate'][b]:.1f} per cent, and the payment {H['pay'][b]:,.0f} dollars: "
             f"{up:.0f} per cent more for nearly the same house. The house barely changed. The loan did.",
             base=[houses, tag, src], steps=[left, right])

    def real(self):
        H = R["hook"]
        ch = line_chart({"house prices against all prices": (H["real"], HOUSE)}, x=(1987, 2025),
                        y=(0.8, 1.9), xticks=[1987, 1995, 2000, 2006, 2012, 2020, 2025], yticks=[0.8, 1.0, 1.2, 1.4, 1.6, 1.8],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="American house prices divided by consumer prices, 1987 = 1",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        one = DashedLine(ch.ax.c2p(1987, 1), ch.ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        p = H["peak06"]
        m1 = marker(ch.ax, p, H["real"][p], f"{p}: x{H['real'][p]:.2f}", BAD, side=UP)
        m2 = marker(ch.ax, 2025, H["real"][2025], f"2025: x{H['real'][2025]:.2f}", HOUSE, side=LEFT)
        src = source("S&P CoreLogic Case-Shiller U.S. National Home Price Index; BLS CPI-U; annual averages via FRED", size=12)
        beat(self,
             "And over forty years. <bookmark mark='a'/> American house prices, divided by all consumer prices, rose to a "
             f"peak in {p}, {H['real'][p]:.2f} times their 1987 level, then fell by a third in the crash. "
             f"<bookmark mark='b'/> By 2025 they were higher than ever: {H['real'][2025]:.2f} times. And, as chapter four "
             "shows, they rose faster than the cost of the materials that go into a house.",
             base=[ch.frame, one, src], steps=[[ch.lines["house prices against all prices"], m1], m2])

    def three(self):
        g = VGroup(VGroup(draw.house_frame(1.8), tx("the house", 22, HOUSE, bold=True)).arrange(DOWN, buff=0.25),
                   VGroup(draw.plot_lot(1.8), tx("the land", 22, LAND, bold=True)).arrange(DOWN, buff=0.25),
                   VGroup(draw.house_key(1.4), tx("the loan", 22, LOAN, bold=True)).arrange(DOWN, buff=0.45)
                   ).arrange(RIGHT, buff=1.6).move_to([0, 0.3, 0])
        beat(self,
             "So where does the price of a house come from? <bookmark mark='a'/> Partly from the house itself: timber, "
             "concrete, wiring, and the trades who put them together. <bookmark mark='b'/> Partly from the land under it, "
             "which cannot be made in a factory and which towns decide how much of to allow. <bookmark mark='c'/> And "
             "partly from the loan, because almost nobody pays for a house with money they already have. This film takes "
             "the three in turn, with the companies that build, lend and sell.",
             base=[], steps=[g[0], g[1], g[2]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-five: homes. Where does the price of a house come from: the house, the "
                            "land or the loan?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()

    def newprice(self):
        E = R["extra"]["newp"]
        ch = line_chart({"median new house": ({y: v / 1e3 for y, v in E.items()}, HOUSE)}, x=(1963, 2025), y=(0, 450),
                        xticks=[1963, 1975, 1985, 1995, 2005, 2015, 2025], yticks=[0, 100, 200, 300, 400],
                        yfmt=lambda v: f"${v:.0f}k", ylabel="median price of a new house sold in America", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 1963, E[1963] / 1e3, f"1963: ${E[1963] / 1e3:.0f}k", ALL, side=UP)
        m2 = marker(ch.ax, 2022, E[2022] / 1e3, f"2022: ${E[2022] / 1e3:.0f}k", BAD, side=UP)
        m3 = marker(ch.ax, 2025, E[2025] / 1e3, f"2025: ${E[2025] / 1e3:.0f}k", HOUSE, side=RIGHT)
        src = source("Census Bureau and HUD, median sales price of new houses sold (annual averages of monthly figures), via FRED", size=12)
        beat(self,
             "In plain dollars, the climb is steeper still. <bookmark mark='a'/> In 1963 the median new house in America "
             f"sold for about {E[1963] / 1e3:.0f} thousand dollars. <bookmark mark='b'/> In 2022 it peaked at about "
             f"{E[2022] / 1e3:.0f} thousand, <bookmark mark='c'/> and in 2025 it was {E[2025] / 1e3:.0f} thousand: a little "
             "lower, as builders, D.R. Horton among them, cut prices and the sizes of their homes to keep buyers able to "
             "pay.",
             base=[ch.frame, src], steps=[[ch.lines["median new house"], m1], m2, m3])
