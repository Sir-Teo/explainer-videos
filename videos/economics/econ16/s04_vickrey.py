from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Vickrey(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Vickrey: \ bid your value", r"In a second-price auction, \ why is bidding exactly your value "
             r"best, \ whatever anyone else does?", "Chapter three. Vickrey: bid your value.",
             lit={1797: r"Goethe's sealed offer", 1961: r"Vickrey", 1990: r"Rothkopf, Teisberg and Kahn"},
             scale=("person",), horizon=("a day",))
        self.history()
        self.proof()
        self.rare()

    def history(self):
        hc = history_card(1961, r"William Vickrey, \ Columbia University", r"``Counterspeculation, Auctions, and "
                          r"Competitive Sealed Tenders''", color=SECOND, width=11.4, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"his question: \ how can a seller get buyers to reveal what a thing is worth to them?",
                  font_size=24),
            label(r"his answer: \ let the winner pay not its own bid, \ but the next one down", font_size=24,
                  color=SECOND),
            label(r"then your bid decides only whether you win, \ never what you pay", font_size=24, color=YOU),
            label(r"the Nobel prize in 1996, \ shared with James Mirrlees; \ Vickrey died three days after it was "
                  r"announced", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Vickrey, J. Finance 16(1) (1961)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1961 William Vickrey, an economist at Columbia, published a paper on auctions in the Journal of "
            "Finance. <bookmark mark='a'/> His question was how a seller could get buyers to reveal what a thing was "
            "worth to them, when each has every reason to hide it. <bookmark mark='b'/> His answer was to let the "
            "winner pay not its own bid, but the next one down. <bookmark mark='c'/> Then your bid decides only "
            "whether you win, never what you pay. <bookmark mark='d'/> The paper was little read for years. In 1996 "
            "it shared the Nobel prize, with James Mirrlees's work on taxes, and Vickrey died three days after the "
            "prize was announced."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def proof(self):
        v = 70.0
        nl = NumberLine(x_range=[0, 100, 10], length=11.0, include_numbers=True, font_size=22, color=GREY_B)
        nl.move_to(DOWN * 0.2)

        def X(x):
            return nl.n2p(x)

        you = VGroup(Line(X(v) + DOWN * 0.3, X(v) + UP * 0.9, color=YOU, stroke_width=5),
                     label(r"your value, \ 70", font_size=20, color=YOU).next_to(X(v) + UP * 0.9, UP, buff=0.08))
        head = label(r"m: \ the highest of the other bids, \ which you can't see", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)

        def band(a_, b_, color):
            return Rectangle(width=abs(X(b_)[0] - X(a_)[0]), height=0.5, stroke_width=0, fill_color=color,
                             fill_opacity=0.45).move_to((X(a_) + X(b_)) / 2)

        hi = VGroup(band(v, 85, HOLD),
                    Line(X(85) + DOWN * 0.3, X(85) + UP * 0.5, color=HOLD, stroke_width=4),
                    label(r"bid 85", font_size=19, color=HOLD).next_to(X(85) + UP * 0.5, UP, buff=0.06))
        lo = VGroup(band(55, v, FIRST),
                    Line(X(55) + DOWN * 0.3, X(55) + UP * 0.5, color=FIRST, stroke_width=4),
                    label(r"bid 55", font_size=19, color=FIRST).next_to(X(55) + UP * 0.5, UP, buff=0.06))
        case1 = VGroup(
            label(r"bid above your value: \ it changes the outcome only if m is between 70 and 85", font_size=22,
                  color=HOLD),
            label(r"and then you win, \ paying m: \ more than the canoe is worth to you", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.1).next_to(nl, DOWN, buff=0.75)
        case2 = VGroup(
            label(r"bid below your value: \ it changes the outcome only if m is between 55 and 70", font_size=22,
                  color=FIRST),
            label(r"and then you lose a canoe you'd have bought for less than it's worth", font_size=22,
                  color=FIRST),
        ).arrange(DOWN, buff=0.1).next_to(nl, DOWN, buff=0.75)
        verdict = label(r"bidding your value is never worse, \ and sometimes better: \ a dominant strategy",
                        font_size=27, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        m = ValueTracker(30.0)
        dot = always_redraw(lambda: VGroup(Dot(X(m.get_value()), radius=0.11, color=WHITE),
                                           label(r"m", font_size=24).next_to(X(m.get_value()) + UP * 0.28, UP, buff=0.04)))
        with self.voiceover(
            "Here is Vickrey's argument, for sale B. Your value is seventy. Call the highest of the other bids m: you "
            "can't see it, and it could be anywhere. <bookmark mark='a'/> First, suppose you bid more than your "
            "value: eighty-five, say. If m is below seventy, you win either way and pay m either way, since the price "
            "is never your own bid. If m is above eighty-five, you lose either way. <bookmark mark='b'/> The higher "
            "bid changes things only when m falls between seventy and eighty-five. Then you win, and pay m, which is "
            "more than the canoe is worth to you. Overbidding can only cost you. <bookmark mark='c'/> Now suppose you "
            "bid less: fifty-five. It changes things only when m falls between fifty-five and seventy. Then you "
            "lose a canoe you would have bought for less than it's worth. Underbidding can only cost you too. "
            "<bookmark mark='d'/> So bidding your value is never worse than any other bid, and sometimes better: "
            "whatever the others bid, however many they are, and whatever you believe about them. Game theorists "
            "call that a dominant strategy."
        ) as vo:
            self.play(FadeIn(nl), FadeIn(you), FadeIn(head))
            self.add(dot)
            self.play(m.animate.set_value(92), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(hi[1:]), m.animate.set_value(50), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hi[0]), m.animate.set_value(78), FadeIn(case1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeOut(hi), FadeOut(case1), FadeIn(lo), FadeIn(case2), m.animate.set_value(62), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(verdict))
        self.clear_scene()

    def rare(self):
        hc = history_card(1797, r"Goethe and his publisher", r"a sealed offer, \ judged against a price Goethe "
                          r"had left, sealed, with a go-between", color=FIRST, width=11.0, font_size=23).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"if the offer beat Goethe's price, \ the publisher would pay Goethe's price: \ a second-price "
                  r"rule", font_size=22),
            label(r"the publisher offered exactly Goethe's price: \ had the go-between told him?",
                  font_size=22,
                  color=HOLD),
            label(r"why Vickrey's auction is rare \ (Rothkopf, \ Teisberg and Kahn, \ 1990):", font_size=24,
                  color=E.ACCENT),
            label(r"a bidder must trust that the seller won't invent a second bid just below the first", font_size=22,
                  color=GREY_A),
            label(r"and must be willing to write down, \ for the seller to see, \ its true value", font_size=22,
                  color=GREY_A),
            label(r"the English clock does the same job \ in the open, \ with nothing to trust", font_size=22,
                  color=SECOND),
        ).arrange(DOWN, buff=0.3).next_to(hc, DOWN, buff=0.4)
        tag = published_tag(r"Moldovanu and Tietzel, JPE 106(4) (1998); \ Rothkopf, Teisberg and Kahn, JPE 98(1) "
                            r"(1990)", corner=DR, font_size=12)
        with self.voiceover(
            "The idea had been tried before Vickrey, by a poet. <bookmark mark='a'/> In 1797 Goethe offered a new "
            "poem to a publisher on a curious condition: the publisher would send a sealed offer, and Goethe left a "
            "price of his own, sealed, with a go-between. If the offer beat Goethe's price, the publisher would pay Goethe's "
            "price, not the offer. That is a second-price rule. <bookmark mark='b'/> It failed for an all too human "
            "reason. The publisher offered exactly Goethe's price, to the thaler, and historians "
            "have wondered ever since whether the go-between told him what it was. "
            "<bookmark mark='c'/> Trust is why Vickrey's auction is rare, as Michael Rothkopf and his co-authors "
            "argued in 1990. <bookmark mark='d'/> A bidder must trust that the seller won't invent a second bid just "
            "below the first. <bookmark mark='e'/> And it must be willing to write down its true value, for the "
            "seller and perhaps its rivals to see. <bookmark mark='f'/> The English clock does the same job in the "
            "open, with nothing to trust, and that is the version the world mostly uses."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
