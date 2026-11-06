from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Auctions(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Mechanism design", r"Can rules make honesty the best policy?", lit=(1961, 1981),
                            part=PART)
        with self.voiceover("Chapter twelve. Mechanism design."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.revelation()
        self.vickrey()
        self.equivalence()
        self.myerson()

    def revelation(self):
        head = label(r"Game theory in reverse", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the question", r"not `what will players do in this game?' \ but `which game should we build, \ so "
                                  r"that what they do is good?'", INST),
                (r"the revelation principle", r"whatever any mechanism achieves in equilibrium, \ a direct mechanism "
                                              r"achieves by asking players their types, \ in which telling the truth is "
                                              r"optimal \ (Gibbard, \ 1973; \ Myerson, \ 1979)", GOAL),
                (r"so", r"we may look only at mechanisms where honesty is a best response", ROW),
                (r"Hurwicz, \ Maskin, \ Myerson", r"the Nobel prize of 2007, \ for laying the theory's foundations",
                 HIST)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4)
        with self.voiceover(
            "Mechanism design runs game theory backward. <bookmark mark='a'/>Instead of asking what players will do "
            "in a given game, it asks which game to build, so that what self-interested players do is good. "
            "<bookmark mark='b'/>Its first theorem is the revelation principle, due to Allan Gibbard and Roger "
            "Myerson among others: whatever outcome any mechanism achieves in equilibrium, some direct mechanism, "
            "which simply asks each player for her private information, achieves too, with truth-telling optimal. "
            "<bookmark mark='c'/>So designers may restrict attention to mechanisms in which honesty is a best "
            "response. <bookmark mark='d'/>Leonid Hurwicz, Eric Maskin and Myerson shared the Nobel prize in 2007 "
            "for the theory."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def vickrey(self):
        d = load("auctions")
        head = label(r"The second-price auction \ (Vickrey, \ 1961)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["value"] == 0.6 and abs(d["best_bid_second"] - 0.6) < 1e-9
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 0.2, 0.05], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True,
                               "decimal_number_config": {"num_decimal_places": 2}}).move_to([-2.4, -0.6, 0])
        xl = label(r"your bid", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"expected gain, \ value 0.6", font_size=16, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        c = VMobject(color=COOP, stroke_width=3).set_points_smoothly([ax.c2p(b, u) for b, u in zip(d["bids"],
                                                                                            d["u_second"])])
        peak = Dot(ax.c2p(0.6, max(d["u_second"])), radius=0.09, color=WHITE)
        side = stack([(r"the highest bid wins, \ and pays the second-highest bid", GREY_A),
                      (r"your bid decides only whether you win, \ never what you pay", COOP),
                      (r"bid above your value: \ you sometimes win and pay more than it is worth", BAD),
                      (r"bid below: \ you sometimes lose an auction you would have liked to win", BAD),
                      (r"truth is a dominant strategy: \ simulated, \ the gain peaks at the bid 0.6", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=4.8, buff=0.26).move_to([4.2, -0.3, 0])
        with self.voiceover(
            "William Vickrey's auction of 1961 is the model. <bookmark mark='a'/>Sealed bids; the highest bid wins, "
            "but pays only the second highest. <bookmark mark='b'/>Your bid then decides only whether you win, never "
            "what you pay. <bookmark mark='c'/>Bidding above your value only adds cases where you win and pay more "
            "than the object is worth to you. <bookmark mark='d'/>Bidding below only adds cases where you lose an "
            "object you would gladly have bought at the price. <bookmark mark='e'/>So bidding your true value is a "
            "dominant strategy. The Reasoner simulates four hundred thousand auctions against a rival with a "
            "uniform value: for a bidder who values the object at point six, expected gain peaks exactly at the bid "
            "point six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            for mk, r in zip("bcd", side[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(c), run_time=1.5)
            self.play(FadeIn(peak), FadeIn(side[4]))
        self.clear_scene()

    def equivalence(self):
        d = load("auctions")
        head = label(r"First price, \ and revenue equivalence", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert abs(d["best_bid_first"] - 0.3) < 1e-9
        assert (d["revenue_second"], d["revenue_first"]) == (0.3331, 0.3331)
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 0.2, 0.05], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True,
                               "decimal_number_config": {"num_decimal_places": 2}}).move_to([-2.4, -0.6, 0])
        xl = label(r"your bid", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        c1 = VMobject(color=COOP, stroke_width=2, stroke_opacity=0.5).set_points_smoothly(
            [ax.c2p(b, u) for b, u in zip(d["bids"], d["u_second"])])
        # above the value 0.6 a first-price win loses money: the curve stops where it meets the axis
        c2 = VMobject(color=MONEY, stroke_width=3).set_points_smoothly([ax.c2p(b, u) for b, u in zip(d["bids"],
                                                                                              d["u_first"])
                                                                         if b <= 0.6 + 1e-9])
        peak = Dot(ax.c2p(0.3, max(d["u_first"])), radius=0.09, color=WHITE)
        ll = VGroup(label(r"second price", font_size=15, color=COOP).next_to(ax.c2p(0.62, 0.17), RIGHT, buff=0.05),
                    label(r"first price", font_size=15, color=MONEY).next_to(ax.c2p(0.3, 0.1), LEFT, buff=0.15))
        side = stack([(r"first price: \ the winner pays her own bid", GREY_A),
                      (r"against a rival bidding half her value, \ the best bid is half yours: \ 0.3", MONEY),
                      (r"expected revenue: \ second price 0.333, \ first price 0.333", GOAL),
                      (r"revenue equivalence \ (Vickrey; \ Myerson, \ 1981): \ same winner, \ same expected price",
                       INST)], font_size=18, aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.2, -0.3, 0])
        with self.voiceover(
            "In a first-price auction the winner pays her own bid, and nobody should bid her value. "
            "<bookmark mark='a'/>Against a rival who bids half his value, the Reasoner's bidder does best by bidding "
            "half of hers: point three. <bookmark mark='b'/>Now compare the seller's revenue. With two bidders whose "
            "values are uniform, the second-price auction raises a third on average; the first-price auction, with "
            "everyone shading, raises a third as well. <bookmark mark='c'/>This is revenue equivalence, proved in "
            "general by Myerson in 1981: any two auctions that give the object to the highest value, and nothing to "
            "a bidder of the lowest value, raise the same expected revenue."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), Create(c1), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(c2), FadeIn(peak), FadeIn(ll), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def myerson(self):
        d = load("auctions")
        head = label(r"Myerson's optimal auction \ (1981)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["revenue_reserve"] == 0.4161 and d["theory"] == [0.3333, 0.4167]
        f = MathTex(r"\psi(v) \;=\; v - \frac{1 - F(v)}{f(v)} \;=\; 2v - 1 \quad (\text{uniform on } [0, 1])",
                    font_size=32, color=INST).move_to([0, 1.6, 0])
        fl = label(r"virtual value: \ sell only to a bidder whose virtual value is positive: \ $v > 1/2$",
                   font_size=19, color=GREY_A).next_to(f, DOWN, buff=0.25)
        hd = [r"\text{auction}", r"\text{expected revenue}", r"\text{theory}"]
        cells = [[label(r"second price, \ no reserve", font_size=18), label(f"{d['revenue_second']:.4f}",
                                                                          font_size=19, color=GREY_A),
                  label(r"1/3", font_size=19)],
                 [label(r"second price, \ reserve 1/2", font_size=18), label(f"{d['revenue_reserve']:.4f}",
                                                                          font_size=19, color=OK),
                  label(r"5/12", font_size=19)]]
        grid = ValueGrid(hd, cells, col_w=[4.2, 3.2, 1.8], cell_h=0.6, font_size=18).move_to([0, -0.6, 0])
        foot = stack([(r"a reserve price raises revenue by 25\%, \ at the cost of sometimes not selling at all", MONEY),
                      (r"revenue and efficiency pull apart: \ the designer's goal matters", BAD)], font_size=19,
                     buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Which auction should a seller use? Myerson answered that too. <bookmark mark='a'/>Replace each bidder's "
            "value by a virtual value, which for uniform values is two v minus one. The revenue of any auction is the "
            "expected virtual value of the winner. So the seller should sell only to a bidder whose virtual value is "
            "positive: in the second-price auction, set a reserve price of a half. <bookmark mark='b'/>The Reasoner "
            "checks: without a reserve, revenue point three three three; with it, point four one six, against five "
            "twelfths in theory. <bookmark mark='c'/>A quarter more revenue, at the cost of sometimes not selling at "
            "all, even when a bidder values the object. Revenue and efficiency pull apart, and the designer has to "
            "choose."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
