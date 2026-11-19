from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


def bidders_panel(c, center, height=4.0, top=100.0, width=7.0):
    """Four bidders as columns: each value as a marked height on a shared scale, the islander under it."""
    names = c["names"]
    vals = c["values"]
    x0 = center[0] - width / 2 + width / 8
    dx = width / 4
    y0 = center[1] - height / 2

    def Y(v):
        return y0 + height * v / top

    cols = VGroup()
    for i, (k, v) in enumerate(zip(names, vals)):
        x = x0 + i * dx
        rail = Line([x, y0, 0], [x, Y(top), 0], color=GREY_D, stroke_width=2)
        col = island.CAST[k].color
        mark = VGroup(Line([x - 0.38, Y(v), 0], [x + 0.38, Y(v), 0], color=col, stroke_width=5),
                      label(rf"{v:.0f}", font_size=18, color=col).next_to([x + 0.38, Y(v), 0], RIGHT, buff=0.08))
        who = islander(k, 0.5).next_to([x, y0, 0], DOWN, buff=0.12)
        cols.add(VGroup(rail, mark, who))
    scale = VGroup(*[label(rf"{t}", font_size=14, color=GREY_B).move_to([x0 - 0.75, Y(t), 0])
                     for t in (0, 25, 50, 75, 100)])
    g = VGroup(cols, scale)
    g.Y, g.x0, g.dx, g.width = Y, x0, dx, width
    return g


class Formats(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Four formats, \ two games", r"Open or sealed, \ rising or falling: \ which auctions are "
             r"really the same?", "Chapter two. Four formats, two games.",
             lit={1961: r"Vickrey", 1995: r"eBay"}, scale=("person", "market"), horizon=("a day",))
        self.four()
        self.english()
        self.dutch()
        self.pairs()

    def four(self):
        rows = point_cards([
            (r"English", r"open; \ the price rises \\ until one bidder is left", SECOND),
            (r"Dutch", r"open; \ the price falls \\ until someone takes it", FIRST),
            (r"first-price sealed", r"one bid each; \ the highest \\ wins, \ and pays its bid", FIRST),
            (r"second-price sealed", r"one bid each; \ the highest \\ wins, \ and pays the next bid", SECOND),
        ], width=12.0, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = label(r"the four standard auctions", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"art rooms; \ the flower clocks of Aalsmeer; \ government tenders; \ Vickrey's 1961 paper",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Economists start from four ways to sell one thing. <bookmark mark='a'/> In the English auction the "
            "price rises, in the open, and bidders drop out until one is left, who pays the price at which the last "
            "rival quit. It is the auction of the art rooms. <bookmark mark='b'/> In the Dutch auction a clock starts "
            "high and falls, and the first bidder to stop it takes the lot at that price. The great flower markets "
            "at Aalsmeer in the Netherlands were built on such clocks. <bookmark mark='c'/> In the first-price sealed "
            "auction, sale A of the last chapter, each bidder writes one bid, and the highest wins and pays it. "
            "Governments buy that way, with tenders. <bookmark mark='d'/> And in the second-price sealed auction, sale "
            "B, the highest bid wins but pays the next bid down. William Vickrey described it in 1961; it is rarer "
            "than the others, though eBay's automatic bidding works much like it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", rows.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def english(self):
        c = load("clock")
        panel = bidders_panel(c, (-2.2, -0.1, 0), height=4.3)
        Y, x0, dx, w = panel.Y, panel.x0, panel.dx, panel.width
        price = ValueTracker(0.0)
        line = always_redraw(lambda: DashedLine([x0 - 0.5, Y(price.get_value()), 0],
                                                [x0 + 3 * dx + 0.5, Y(price.get_value()), 0], color=SECOND,
                                                stroke_width=3))
        tick = always_redraw(lambda: label(rf"price \ {price.get_value():.0f}", font_size=20, color=SECOND).next_to(
            [x0 + 3 * dx + 0.5, Y(price.get_value()), 0], RIGHT, buff=0.15))
        head = label(r"the English clock: \ the price rises", font_size=28, color=SECOND).to_edge(UP, buff=0.35)
        side = VGroup(
            label(r"each stays in \\ until the price \\ reaches their value", font_size=21, color=GREY_A),
            label(rf"Bo wins, \\ and pays {c['english_price']:.0f}: \\ the second-highest value", font_size=23,
                  color=SECOND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5)
        drops = c["english_drops"]
        order = [int(k) for k in sorted(drops, key=lambda k: drops[k])]
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Watch one sale on each clock. Ana values the canoe at thirty-one shells, Bo at eighty-four, Dara at "
            "fifty-seven, and Friday at seventy-two. <bookmark mark='a'/> On the English clock the price rises from "
            "nothing. Each bidder stays in until the price reaches their value, since staying longer could only win "
            "the canoe at a loss, and leaving sooner could only give up a bargain. <bookmark mark='b'/> Ana drops "
            "out at thirty-one, Dara at fifty-seven, and Friday at seventy-two. <bookmark mark='c'/> Bo is left, and "
            "pays seventy-two: the second-highest value."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panel), FadeIn(tag))
            self.add(line, tick)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            for i in order:
                self.play(price.animate.set_value(drops[str(i)] if str(i) in drops else drops[i]), run_time=1.6,
                          rate_func=linear)
                self.play(panel[0][i].animate.set_opacity(0.25), run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), Indicate(panel[0][c["english_winner"]][1], color=WHITE))
        self.clear_scene()

    def dutch(self):
        c = load("clock")
        panel = bidders_panel(c, (-2.2, -0.1, 0), height=4.3)
        Y, x0, dx = panel.Y, panel.x0, panel.dx
        plan = VGroup()
        for i, b in enumerate(c["dutch_bids"]):
            x = x0 + i * dx
            plan.add(VGroup(DashedLine([x - 0.3, Y(b), 0], [x + 0.3, Y(b), 0], color=FIRST, stroke_width=3),
                            label(rf"{b:.0f}", font_size=15, color=FIRST).next_to([x - 0.3, Y(b), 0], LEFT,
                                                                                  buff=0.06)))
        price = ValueTracker(100.0)
        line = always_redraw(lambda: DashedLine([x0 - 0.5, Y(price.get_value()), 0],
                                                [x0 + 3 * dx + 0.5, Y(price.get_value()), 0], color=FIRST,
                                                stroke_width=3))
        tick = always_redraw(lambda: label(rf"price \ {price.get_value():.0f}", font_size=20, color=FIRST).next_to(
            [x0 + 3 * dx + 0.5, Y(price.get_value()), 0], RIGHT, buff=0.15))
        head = label(r"the Dutch clock: \ the price falls", font_size=28, color=FIRST).to_edge(UP, buff=0.35)
        side = VGroup(
            label(r"each plans a price \\ at which to stop it: \\ a little below their value", font_size=21,
                  color=GREY_A),
            label(r"nothing is learned \\ while the clock falls: \\ the plan is a sealed bid", font_size=21,
                  color=GREY_A),
            label(rf"Bo stops it at {c['dutch_price']:.0f}, \\ and pays that", font_size=23, color=FIRST),
            label(rf"this time \ {c['dutch_price']:.0f} \ against \ {c['english_price']:.0f}: \\ on average, \ the "
                  r"same", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now the same four on the Dutch clock, which starts at a hundred and falls. <bookmark mark='a'/> Stopping "
            "the clock at your value would win, but gain nothing. So each bidder plans a price a little below their "
            "value at which to stop it, the dashed marks, trading a better price against the risk that someone stops "
            "it first. <bookmark mark='b'/> And while the clock falls, nobody learns anything, because the first "
            "bidder to move ends the sale. So the plan is all there is: it is a sealed bid. <bookmark mark='c'/> "
            "Bo's plan is the highest, sixty-three, and Bo pays sixty-three. <bookmark mark='d'/> This time the "
            "Dutch clock raised less than the English one. Chapter five shows that, on average, they raise the "
            "same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panel), FadeIn(tag))
            self.add(line, tick)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(plan))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(price.animate.set_value(c["dutch_price"]), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(plan[c["dutch_winner"]], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def pairs(self):
        left = VGroup(
            label(r"Dutch \ $=$ \ first-price sealed", font_size=30, color=FIRST),
            label(r"the same game exactly: \ a plan is a price, \\ and nothing is learned before it is used",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2)
        right = VGroup(
            label(r"English \ $\approx$ \ second-price sealed", font_size=30, color=SECOND),
            label(r"with private values: \ stay in to (or bid) your value; \\ the winner pays the second value",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(DOWN, buff=0.8).move_to(UP * 0.3)
        head = label(r"four formats, \ two games", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"the English clock shows who quits, \ and when: \ that matters when values are shared "
                     r"(chapters six and eight)", font_size=21, color=HOLD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So the four formats are two games. <bookmark mark='a'/> The Dutch clock and the first-price sealed bid "
            "are the same game exactly: in each, a strategy is a price, chosen before anything is learned. "
            "<bookmark mark='b'/> The English clock and the second-price sealed bid are nearly the same. When each "
            "bidder knows their own value, the best plan in both is to stay in, or bid, up to that value, and the "
            "winner pays the second-highest value. <bookmark mark='c'/> They differ in one way. On the English "
            "clock you see others quit, and when. If the thing has a value shared by everyone, like oil under the "
            "ground, that tells you something, and chapters six and eight are about what."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
