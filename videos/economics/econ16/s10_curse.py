from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Curse(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The winner's curse", r"When a thing is worth the same to everyone, \ but nobody knows how "
             r"much, \ what does winning tell you?", "Chapter eight. The winner's curse.",
             lit={1971: r"Capen, Clapp and Campbell", 1983: r"Bazerman and Samuelson", 1982: r"Milgrom and Weber"},
             scale=("firm", "market"), horizon=("a year",))
        self.oil()
        self.draws()
        self.bars()
        self.jar()
        self.defence()

    def oil(self):
        hc = history_card(1971, r"three engineers at Atlantic Richfield", r"``Competitive Bidding in High-Risk "
                          r"Situations'', \ on the Gulf of Mexico's oil leases", color=CURSE, width=11.6,
                          font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"the oil under a tract is worth much the same to every company: \ a common value", font_size=24),
            label(r"each company's geologists estimate it, \ with error, \ but without bias", font_size=24),
            label(r"the company that wins is the one with the highest estimate", font_size=24, color=CURSE),
            label(r"which is usually one that overestimated", font_size=25, color=HOLD),
            label(r"they called it the winner's curse", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Capen, Clapp and Campbell, J. Petroleum Technology 23 (1971)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Through the 1960s, oil companies bid for the right to drill in the Gulf of Mexico, and year after year "
            "the returns on the leases they won disappointed them. In 1971 three engineers at Atlantic Richfield, "
            "Edward Capen, Robert Clapp and William Campbell, offered an explanation. <bookmark mark='a'/> The oil "
            "under a tract is worth much the same to every company: a common value, unlike Crusoe's canoe. "
            "<bookmark mark='b'/> Each company's geologists estimate it, with error but without bias: too high as "
            "often as too low. <bookmark mark='c'/> But the company that wins is the one with the highest estimate. "
            "<bookmark mark='d'/> And the highest of many honest estimates is usually too high. "
            "<bookmark mark='e'/> They called it the winner's curse."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def draws(self):
        c = load("curse")
        V, s = c["value"], c["noise"]
        rng = np.random.default_rng(1971)
        nl = NumberLine(x_range=[5, 15, 1], length=11.0, include_numbers=True, font_size=20, color=GREY_B)
        nl.move_to(DOWN * 0.3)
        true = VGroup(Line(nl.n2p(V) + DOWN * 0.3, nl.n2p(V) + UP * 2.6, color=PRICE, stroke_width=4),
                      label(r"the true value, \ 10", font_size=19, color=PRICE).next_to(nl.n2p(V) + UP * 2.6, UP,
                                                                                    buff=0.08))
        head = label(r"each bidder's estimate: \ the true value, \ give or take up to 3", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.4)

        def row(n, y, color):
            e = V + rng.uniform(-s, s, n)
            dots = VGroup(*[Dot(nl.n2p(x) + UP * y, radius=0.08, color=color) for x in e])
            k = int(np.argmax(e))
            ring = Circle(radius=0.17, color=HOLD, stroke_width=3).move_to(dots[k])
            tag_ = label(rf"n = {n}: \ the winner's estimate, \ {e[k]:.1f}", font_size=18, color=HOLD).next_to(
                ring, UP, buff=0.12)
            return dots, ring, tag_

        d4 = row(4, 0.7, RIVALS[0])
        d16 = row(16, 1.7, RIVALS[3])
        foot = label(r"the winner is whoever erred the most upward", font_size=25, color=E.ACCENT).to_edge(DOWN,
                                                                                                buff=0.6)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora can show it. A tract is worth ten, and each bidder's estimate is ten, give or take up to three, "
            "with every error in that range equally likely. <bookmark mark='a'/> Here are four bidders' estimates. "
            "The highest wins. <bookmark mark='b'/> Here are sixteen. With more bidders, the highest estimate is "
            "further above the truth. <bookmark mark='c'/> The winner is not the bidder who saw most clearly; it is "
            "the one who erred most upward."
        ) as vo:
            self.play(FadeIn(nl), FadeIn(true), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in d4[0]], lag_ratio=0.2))
            self.play(Create(d4[1]), FadeIn(d4[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in d16[0]], lag_ratio=0.08))
            self.play(Create(d16[1]), FadeIn(d16[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bars(self):
        c = load("curse")
        rows = c["rows"]
        ax = plane([-0.6, 4.6], [0, 3.2], center=LEFT * 2.4 + DOWN * 0.35, x_length=7.0, y_length=4.6, xticks=[],
                   yticks=[0, 1, 2, 3], ylabel=r"the winner's overestimate", font_size=16, yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, r in enumerate(rows):
            lo, hi = a.c2p(i - 0.3, 0), a.c2p(i + 0.3, r["overestimate"])
            b = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=CURSE,
                          fill_opacity=0.85).move_to((lo + hi) / 2)
            bars.add(b)
            labs.add(label(rf"{r['n']} bidders", font_size=17, color=GREY_A).next_to(a.c2p(i, 0), DOWN, buff=0.15))
            vals.add(label(rf"{r['overestimate']:.2f}", font_size=17, color=CURSE).next_to(b, UP, buff=0.08))
        cap = VGroup(DashedLine(a.c2p(-0.6, 3), a.c2p(4.6, 3), color=GREY_C, stroke_width=2),
                     label(r"the largest possible error", font_size=15, color=GREY_B).next_to(a.c2p(4.6, 3), UP,
                                                                                         buff=0.08).shift(LEFT * 1.2))
        side = VGroup(
            MathTex(r"\mathbb{E}[\text{overestimate}] = 3\,\frac{n-1}{n+1}", font_size=32, color=CURSE),
            label(r"bid your honest estimate, \\ and you lose that much \\ on average, \ when you win", font_size=21,
                  color=HOLD),
            label(r"so with a common value, \\ more rivals mean \ bid less", font_size=22, color=E.ACCENT),
            label(r"the opposite of chapter four", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is the winner's average overestimate, from forty thousand tracts for each number of bidders. "
            "<bookmark mark='a'/> With two bidders it is one; with four, one point eight; with thirty-two, almost "
            "the largest error possible. The formula is three times n minus one over n plus one. "
            "<bookmark mark='b'/> A bidder who bids its honest estimate loses that much, on average, whenever it "
            "wins. <bookmark mark='c'/> So when a value is shared, more rivals mean you should bid less, not more: "
            "winning against many is worse news than winning against few. <bookmark mark='d'/> That is the opposite "
            "of chapter four, where more rivals meant shading less."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(cap), FadeIn(tag))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(vals), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def jar(self):
        fa = facts.BY_KEY["winners_curse"]
        j = load("curse")["jar"]
        guess = label(r"(yours: \ bidding for a jar of coins, \\ would you bid above \\ your own estimate?)",
                      font_size=21, color=E.ACCENT)
        data_col = VGroup(
            label(rf"each jar: \ \${j['value']:.2f}", font_size=21),
            label(rf"average estimate: \ \${j['mean_estimate']:.2f}", font_size=21, color=GREY_A),
            label(rf"average winning bid: \ \${j['mean_winning_bid']:.2f}", font_size=21, color=HOLD),
            label(rf"the winner's average loss: \ \${j['mean_loss']:.2f}", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ag = VGroup(
            label(r"bid your estimate, \\ lose $3\,\tfrac{n-1}{n+1}$", font_size=21, color=CURSE),
            label(r"more bidders, \ bigger loss", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fc = fact_card(fa.statement, columns=((r"your guess", guess), (r"the data", data_col), (r"Agora", ag)),
                       width=12.6).move_to(UP * 0.8)
        rows = VGroup(
            label(rf"{j['auctions']} auctions in {j['classes']} MBA classes: \ the estimates were too low, \ on "
                  r"average, \ and the winners still lost", font_size=22),
            label(r"the curse needs no optimists: \ only many estimates, \ and the highest one winning",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.15).next_to(fc, DOWN, buff=0.55)
        tag = published_tag(r"Bazerman and Samuelson, JCR 27(4) (1983)", corner=DR, font_size=13)
        with self.voiceover(
            "This is one of the series' Facts: the winners of common-value auctions tend to overpay. "
            "<bookmark mark='a'/> First, a guess: bidding for a jar of coins, would you bid above your own estimate "
            "of what's in it? <bookmark mark='b'/> In a study published in 1983, Max Bazerman and William "
            "Samuelson auctioned jars to MBA students in Boston. Each jar held eight dollars, in pennies, nickels or paper clips worth a few cents "
            "each, and the highest sealed bid won the jar's value and paid its bid. The students' average estimate "
            "was five dollars thirteen, well below the truth. The average winning bid was ten dollars and one cent. "
            "<bookmark mark='c'/> Agora's honest bidders lose, on average, the winner's overestimate, more so the "
            "more bidders there are. <bookmark mark='d'/> Across forty-eight auctions in twelve classes, the students "
            "underestimated the jars on average, and their winners still lost two dollars a jar. "
            "<bookmark mark='e'/> The curse needs no optimists: only many estimates, and the highest one winning."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc.head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def defence(self):
        rows = VGroup(
            label(r"the cure: \ bid as if your estimate were the highest, \ because when you win, \ it is",
                  font_size=24, color=E.ACCENT),
            label(r"the equilibrium shades further still: \ the price a winner pays must be worth it, \ given that it "
                  r"won", font_size=23),
            label(r"an English clock helps: \ rivals who quit reveal their estimates, \ and the winner learns",
                  font_size=23, color=SECOND),
            label(r"Milgrom and Weber's linkage principle: \ the more the price tracks others' information, \ the "
                  r"less the curse", font_size=22, color=SECOND),
            label(r"experienced bidders can learn it; \ in the laboratory, \ novices fall for it, \ and learn only "
                  r"slowly", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Milgrom and Weber, Econometrica 50(5) (1982); \ Kagel and Levin, \emph{Common Value "
                            r"Auctions and the Winner's Curse} (2002)", corner=DR, font_size=12)
        with self.voiceover(
            "What should a bidder do? <bookmark mark='a'/> Bid as if your estimate were the highest, because when "
            "you win, it is. Ask what the thing is worth given that you won, not what it is worth. "
            "<bookmark mark='b'/> The equilibrium bid shades further still: the price must be worth paying given "
            "that you won at it. <bookmark mark='c'/> And an English clock helps, because rivals who quit reveal "
            "something about their estimates, and the winner learns from them. <bookmark mark='d'/> That is Milgrom "
            "and Weber's linkage principle: the more the price a winner pays is tied to other bidders' information, "
            "the less the winner's curse bites, the less bidders need to shade, and the more the seller earns. "
            "<bookmark mark='e'/> Experienced bidders can learn this: the oil engineers wrote their paper to teach "
            "it. In the laboratory, John Kagel and Dan Levin found that people new to such auctions fall for the "
            "curse, and learn to avoid it only slowly."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
