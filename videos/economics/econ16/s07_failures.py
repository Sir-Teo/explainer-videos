from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Failures(VoiceoverScene):
    def construct(self):
        card(self, 6, r"When equivalence fails", r"Risk, \ the laboratory, \ unequal bidders, \ shared values: \ "
             r"which format wins when?", "Chapter six. When equivalence fails.",
             lit={1982: r"Milgrom and Weber", 1987: r"Kagel, Harstad and Levin", 1988: r"Cox, Smith and Walker",
                  2000: r"Maskin and Riley"}, scale=("person", "market"), horizon=("a day",))
        self.risk()
        self.lab()
        self.table()

    def risk(self):
        r = load("risk")
        vs = np.array(r["vs"])
        ax = plane([0, 1], [0, 1], center=LEFT * 2.8 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"your value",
                   ylabel=r"your first-price bid", font_size=16, xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
        a = ax.ax
        diag = DashedLine(a.c2p(0, 0), a.c2p(1, 1), color=GREY_C, stroke_width=2)
        neu = path(ax, vs, r["neutral"], color=FIRST, width=3, smooth=False)
        ave = path(ax, vs, r["averse"], color=VALUE, width=3, smooth=False)
        l1 = label(r"risk neutral: \ $\tfrac34 v$", font_size=17, color=FIRST).next_to(a.c2p(1, 0.75), RIGHT,
                                                                                    buff=0.1)
        l2 = label(r"risk averse: \ $\tfrac67 v$", font_size=17, color=VALUE).next_to(a.c2p(1, 6 / 7), RIGHT,
                                                                                   buff=0.1)
        side = VGroup(
            label(r"a bidder who dislikes risk \\ pays to lower the chance of losing", font_size=21, color=VALUE),
            label(r"in a second-price auction \\ bidding your value stays best: \\ risk changes nothing", font_size=21,
                  color=SECOND),
            label(rf"revenue, \ first-price: \ {r['first']:.3f}", font_size=22, color=VALUE),
            label(rf"revenue, \ second-price: \ {r['second']:.3f}", font_size=22, color=SECOND),
            label(r"so with risk-averse bidders, \\ pay-your-bid raises more", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "First, risk. Suppose each bidder values money with the square root of its gain, so that a sure five "
            "shells beats an even chance of ten. <bookmark mark='a'/> In a first-price auction, a bidder like that "
            "shades less: with four bidders it bids six sevenths of its value instead of three quarters. It is "
            "paying a little more to lower the chance of losing, as if buying insurance. <bookmark mark='b'/> In a "
            "second-price auction risk changes nothing: bidding your value is still best whatever happens. "
            "<bookmark mark='c'/> So on Agora's same draws, the first-price auction now raises nought point six "
            "eight six, <bookmark mark='d'/> and the second-price auction still nought point six. "
            "<bookmark mark='e'/> With bidders who fear risk, a seller does better to be paid the bids."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), Create(neu), FadeIn(l1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ave), FadeIn(l2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lab(self):
        left = study_card(r"First-price auctions in the laboratory", r"Cox, Smith and Walker (1988), and many since",
                          [(r"design", r"students bid for cash prizes with values drawn at random"),
                           (r"found", r"bids above the risk-neutral equilibrium, \ for most bidders"),
                           (r"read", r"consistent with risk aversion, though not only with it")],
                          design="lab", width=6.0, font_size=20)
        right = study_card(r"Second-price auctions in the laboratory", r"Kagel, Harstad and Levin (1987); \ Kagel "
                           r"and Levin (1993)",
                           [(r"design", r"the same, \ with Vickrey's rule, and with the English clock"),
                            (r"found", r"sealed: \ many bids above value, and it persists"),
                            (r"found", r"English clock: \ close to value, and quickly")],
                           design="lab", width=6.0, font_size=20)
        VGroup(left, right).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.4)
        foot = VGroup(
            label(r"a dominant strategy on paper is not always obvious in practice; \ the clock makes it obvious",
                  font_size=22, color=E.ACCENT),
            label(r"your Play it bids: \ above 52.5 in sale A, \ or above 70 in sale B? \ So are most people's",
                  font_size=22, color=YOU),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Cox, Smith and Walker, J. Risk Uncertainty 1 (1988); \ Kagel, Harstad and Levin, "
                            r"Econometrica 55(6) (1987); \ Kagel and Levin, EJ 103 (1993)", corner=UR, font_size=12)
        with self.voiceover(
            "Economists have watched people bid in laboratories since about 1980, for real money, with values handed "
            "out at random so that the theory's answer is known. <bookmark mark='a'/> In first-price auctions, most "
            "bidders bid above the risk-neutral equilibrium, as James Cox, Vernon Smith and James Walker found. Risk "
            "aversion can explain it, though perhaps not all of it. <bookmark mark='b'/> In second-price auctions "
            "something stranger happens. Bidding your value is dominant, yet in John Kagel's experiments with Ronald "
            "Harstad and Dan Levin, many bids were above value, and the habit persisted. <bookmark mark='c'/> Run "
            "the same auction as an English clock, though, and people stop close to their values, and quickly. "
            "<bookmark mark='d'/> A dominant strategy on paper is not always obvious to a person; the rising clock "
            "makes it obvious, since the moment the price passes your value, you can see that staying in can only "
            "lose. <bookmark mark='e'/> So if your bids in Play it were above fifty-two and a half, or above "
            "seventy, so were most people's."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def table(self):
        head = label(r"when the theorem's assumptions fail, \ which format raises more?", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        rows = [
            (r"bidders fear risk", r"pay-your-bid", r"they shade less to avoid losing", VALUE),
            (r"the seller fears risk", r"pay-your-bid", r"its price varies less", FIRST),
            (r"values are linked \ (Milgrom and Weber)", r"the English clock", r"quitters reveal what they knew",
             SECOND),
            (r"a strong and a weak bidder \ (Maskin and Riley)", r"it depends", r"pay-your-bid helps the weak one, "
             r"\ and can misallocate", GREY_A),
            (r"bidders could collude", r"sealed bids", r"no way to signal or punish in the bidding", HOLD),
            (r"too few would enter", r"sealed bids", r"a weaker bidder has a chance", HOLD),
        ]
        grid = VGroup()
        for cond, fmt_, why, c in rows:
            grid.add(VGroup(label(cond, font_size=21, color=c), label(fmt_, font_size=22, color=WHITE),
                            label(why, font_size=19, color=GREY_A)))
        widths = (4.9, 2.7, 5.2)
        x0 = -6.4
        for i, r in enumerate(grid):
            y = 1.9 - 0.68 * i
            x = x0
            for j, cell in enumerate(r):
                if cell.width > widths[j] - 0.15:
                    cell.scale_to_fit_width(widths[j] - 0.15)
                cell.move_to([x + cell.width / 2, y, 0])
                x += widths[j]
        hdr = VGroup(label(r"if", font_size=20, color=GREY_B).move_to([x0 + 0.1, 2.55, 0], aligned_edge=LEFT),
                     label(r"favours", font_size=20, color=GREY_B).move_to([x0 + widths[0], 2.55, 0],
                                                                           aligned_edge=LEFT),
                     label(r"because", font_size=20, color=GREY_B).move_to([x0 + widths[0] + widths[1], 2.55, 0],
                                                                           aligned_edge=LEFT))
        foot = label(r"no format is best everywhere: \ design starts from who the bidders are", font_size=24,
                     color=E.ACCENT).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Milgrom and Weber, Econometrica 50(5) (1982); \ Maskin and Riley, RES 67(3) (2000); \ "
                            r"Klemperer, JEP 16(1) (2002)", corner=DR, font_size=12)
        with self.voiceover(
            "Put the failures together, and each points somewhere. <bookmark mark='a'/> Bidders who fear risk favour "
            "paying the bids, as we saw, and so does a seller who fears it. <bookmark mark='b'/> When bidders' "
            "values are linked, because each holds a clue to a value they partly share, Paul Milgrom and Robert "
            "Weber showed in 1982 that the English clock raises the most: as rivals quit, they reveal what they "
            "knew, and the remaining bidders, less afraid of overpaying, bid more. <bookmark mark='c'/> When one "
            "bidder is strong and another weak, the answer depends on the details: a first-price auction makes the "
            "strong bidder shade more, which helps the weak one, and can hand the object to the wrong bidder. "
            "<bookmark mark='d'/> And two failures that matter most in practice: when bidders could collude, and "
            "when too few would bother to come. Both favour sealed bids, as chapter ten will show the hard way. "
            "<bookmark mark='e'/> No format is best everywhere. Design starts from who the bidders are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(grid[0]), FadeIn(grid[1]))
            vo.wait_until("b")
            self.play(FadeIn(grid[2]))
            vo.wait_until("c")
            self.play(FadeIn(grid[3]))
            vo.wait_until("d")
            self.play(FadeIn(grid[4]), FadeIn(grid[5]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
