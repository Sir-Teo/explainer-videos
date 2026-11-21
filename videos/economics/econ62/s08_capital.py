from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Capital(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Capital structure", r"How much should a firm borrow?", "Chapter seven. Capital structure.",
             lit={1958: r"Modigliani and Miller", 1984: r"the pecking order", 2001: r"Graham and Harvey"},
             scale=("firm",), horizon=("a decade",))
        self.tradeoff()
        self.practice()

    def tradeoff(self):
        T = load("tradeoff")
        L, V = np.array(T["leverage"]), np.array(T["value"])
        tax = 100.0 + 0.21 * 100.0 * L
        ax = plane([0, 0.95], [95, 122], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75], yticks=[100, 110, 120], xlabel=r"debt, \ share of the firm's value",
                   ylabel=r"the firm's value", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        mm = seg(ax, 0, 100, 0.95, 100, GREY_B, 2.0, dashed=True)
        pt = path(ax, L, tax, GAIN, 2.4)
        pv = path(ax, L, V, FIN, 3.2)
        k = int(np.argmax(V))
        best = dot(ax, L[k], V[k], WHITE, 0.08)
        side = VGroup(
            label(r"grey: \ Modigliani and Miller, \ no taxes and no bankruptcy: \\ the mix of debt and equity does "
                  r"not matter \ (Part 23)", font_size=18, color=GREY_B),
            label(r"green: \ interest is deducted from taxable profit, \\ so debt saves 21 cents of tax a dollar",
                  font_size=18, color=GAIN),
            label(r"pink: \ but debt raises the chance of distress, \\ which destroys value: \ lost customers, \ "
                  r"forced sales, \ lawyers", font_size=18, color=FIN),
            label(rf"the trade-off's best: \ about {100 * T['best']:.0f}\% debt, \ value +{T['gain']:.1f}\%",
                  font_size=20, color=WHITE),
            label(r"real firms borrow less than this, \ and the most profitable least of all", font_size=18,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.org.tradeoff; \ volatility 35\%, \ distress costs 60\% of value",
                        corner=DL, font_size=12)
        with self.voiceover(
            "How much should a firm borrow? <bookmark mark='a'/> Part twenty-three's Modigliani and Miller "
            "theorem is the starting point: with no taxes and no cost of going bust, the mix of debt and equity "
            "changes how the firm's value is divided, not its size. <bookmark mark='b'/> Add taxes: interest is "
            "deducted from taxable profit, so each dollar of debt saves twenty-one cents of tax at today's "
            "American rate. <bookmark mark='c'/> Add distress: the more a firm borrows, the likelier a bad year "
            "pushes it into default, where value is destroyed, by lost customers, forced sales and lawyers. "
            f"<bookmark mark='d'/> Balancing the two, the Island's firm is worth most at about {100 * T['best']:.0f} "
            f"percent debt, {T['gain']:.1f} percent more than with none. <bookmark mark='e'/> That is the "
            "trade-off theory, and its embarrassment is that real firms borrow less than it suggests, and the most "
            "profitable firms, which could carry the most debt, borrow least of all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(mm), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pt), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pv), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(best), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def practice(self):
        chain = flow_chain([(r"retained profits", GAIN), (r"debt", FIN), (r"new shares, \ last", COST)],
                           box_w=3.0, box_h=1.0, buff=0.7, font_size=21).move_to(UP * 2.0)
        why = label(r"the pecking order: \ managers know more than investors, \ so a firm that sells shares \\ "
                    r"signals that it thinks they are overpriced, \ and the price falls \ (Myers and Majluf, \ "
                    r"Part 13)", font_size=19, color=WHITE).next_to(chain, DOWN, buff=0.4)
        cards = point_cards([
            (r"what CFOs say", r"392 chief financial officers: \ for debt, \ financial flexibility and a good credit "
             r"rating matter most", FIN),
            (r"how they invest", r"large firms use net present value and the CAPM; \ small firms often use the "
             r"payback period", OWN),
        ], width=12.0, cols=2, font_size=19).next_to(why, DOWN, buff=0.45)
        tag = published_tag(r"Myers and Majluf, \ JFE 13 (1984); \ Graham and Harvey, \ JFE 60 (2001)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "A second theory explains the embarrassment. <bookmark mark='a'/> Firms finance investment first from "
            "their own profits, then by borrowing, and issue new shares last. <bookmark mark='b'/> Stewart Myers "
            "and Nicholas Majluf's reason is Part thirteen's adverse selection: managers know more than investors, "
            "so a firm that sells shares signals that it thinks they are overpriced, and the price falls. "
            "Profitable firms have their own cash and never need to climb the ladder. <bookmark mark='c'/> And "
            "what do the people who decide say? John Graham and Campbell Harvey surveyed three hundred and "
            "ninety-two chief financial officers: for debt, financial flexibility and a good credit rating mattered "
            "most, more than the tax shield. <bookmark mark='d'/> Large firms used net present value and the "
            "capital asset pricing model, as the textbooks say; small firms often used the payback period, how "
            "long until the money comes back."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in chain.boxes], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in chain.arrows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.1))
        self.clear_scene()
