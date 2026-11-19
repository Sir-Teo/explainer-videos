from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


class Rabin(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Rabin's calibration", r"If you turn down a small bet, what does expected utility say you must "
             r"turn down?", "Chapter nine. Rabin's calibration.", lit={2000: r"Rabin's calibration theorem"})
        self.small_bet()
        self.crra_case()
        self.theorem()
        self.moral()

    def small_bet(self):
        r = load("rabin")
        bet = lottery_card([(r"$\tfrac12$", r"lose \$100"), (r"$\tfrac12$", r"win \$110")], r"a small bet",
                           color=RISKY, width=4.6, font_size=32).move_to(UP * 1.9)
        q = label(r"would you take it?", font_size=32).next_to(bet, DOWN, buff=0.5)
        most = label(r"many people would not", font_size=28, color=GREY_A).next_to(q, DOWN, buff=0.35)
        why = VGroup(
            label(r"expected utility says: \ turning it down means $u$ bends sharply over \$210", font_size=26),
            label(rf"an ordinary chooser ($\gamma = 2$, \ \$100{{,}}000) would take it: \\ he is indifferent at a "
                  rf"gain of \${r['g2_breakeven']:.2f}", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(most, DOWN, buff=0.5)
        with self.voiceover(
            "In 2000 Matthew Rabin asked a deceptively simple question. <bookmark mark='a'/> Here is a bet: lose a "
            "hundred dollars or win a hundred and ten, on the toss of a coin. Would you take it? "
            "<bookmark mark='b'/> Many people wouldn't, and it doesn't seem unreasonable to refuse. "
            "<bookmark mark='c'/> But think about what refusing means under expected utility. For someone with a "
            "hundred thousand dollars, this bet is a tiny ripple in their wealth, and over a range of two hundred "
            "and ten dollars any smooth utility function is almost a straight line. An ordinary chooser, with a gamma "
            "of two, would take the bet with any gain above a hundred dollars and twenty cents. To refuse it, the "
            "utility function must bend sharply over a range of two hundred dollars."
        ) as vo:
            self.play(FadeIn(bet, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(most))
            vo.wait_until("c")
            self.play(FadeIn(why[0]))
            self.play(FadeIn(why[1]))
        self.clear_scene()

    def crra_case(self):
        r = load("rabin")
        head = label(r"how much curvature does refusing take?", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup()
        for x in r["rows"]:
            rows.add(VGroup(label(rf"wealth {big(x['wealth'])}", font_size=27),
                            label(rf"$\gamma$ = {x['gamma']:.0f}", font_size=30, color=RISKY)).arrange(RIGHT, buff=0.8))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.45).shift(LEFT * 3.0)
        big_ = VGroup(
            label(rf"take $\gamma$ = {r['gamma']:.0f} at \$100{{,}}000. \ Then:", font_size=26),
        )
        L = r["losses"]
        for loss, G in zip(L, r["crra_largest"]):
            txt = (rf"lose \${loss:,}".replace(",", "{,}") + r" \ or win " +
                   (r"\emph{any} sum: \ refused" if not np.isfinite(G) else rf"\${G:,.0f}: \ refused".replace(",",
                                                                                                         "{,}")))
            big_.add(label(txt, font_size=25, color=RISKY if not np.isfinite(G) else WHITE))
        big_.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rows, RIGHT, buff=1.0).align_to(rows, UP)
        foot = label(r"constant relative risk aversion, \ computed: \ $\gamma \approx 2W(g-l)/(g^2+l^2)$ for a small "
                     r"bet", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "How sharply? Take the power function and ask what gamma it needs to refuse the bet. "
            "<bookmark mark='a'/> With ten thousand dollars of wealth, a gamma of nine. With a hundred thousand, "
            "ninety-one. With a million, about nine hundred. The needed curvature grows in proportion to wealth, "
            "because the bet shrinks relative to it. <bookmark mark='b'/> Now take someone who refuses the small bet "
            "at a hundred thousand dollars, and so has a gamma of ninety-one, and offer them larger bets. A fifty-fifty "
            "chance of losing four hundred dollars, they'd refuse unless the gain were more than six hundred and "
            "thirty-four. Losing six hundred: they'd refuse any gain up to fourteen hundred. And a fifty-fifty chance "
            "of losing eight hundred dollars, or a thousand, they would refuse whatever the prize. A billion dollars. "
            "<bookmark mark='c'/> That's absurd, and nobody behaves like that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(big_[0]))
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.15) for b_ in big_[1:]], lag_ratio=0.6), run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def theorem(self):
        r = load("rabin")
        q = quote_card(tex_safe(r["example"]), r"Rabin, \emph{Econometrica} (2000), p.\ 1282", width=11.6, font_size=25,
                       color=RISKY).to_edge(UP, buff=0.45)
        t1 = r["table1"]
        head = label(r"Rabin's table I: \ turn down lose \$100 / win \$110 at every wealth; \ then for each loss $L$, "
                     r"the largest gain still turned down", font_size=21, color=GREY_A)
        cells = VGroup()
        for L, G in t1.items():
            cells.add(VGroup(label(rf"\${int(L):,}".replace(",", "{,}"), font_size=26),
                             label(big(float(G)), font_size=26, color=RISKY)).arrange(DOWN, buff=0.15))
        cells.arrange(RIGHT, buff=0.9)
        tab = VGroup(head, cells).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.45)
        t2 = r["table2"]
        note_ = label(rf"even if the small bet is refused only below \$300{{,}}000 of wealth (table II, from "
                      rf"\$290{{,}}000): \\ lose \$1{{,}}000 or win {big(float(t2.get('1000', t2.get(1000))))}: \ refused", font_size=22,
                      color=GREY_A).next_to(tab, DOWN, buff=0.4)
        tag = published_tag(r"Rabin, Econometrica 68(5) (2000), tables I and II", corner=DR, font_size=14)
        with self.voiceover(
            "Rabin's theorem says it isn't a quirk of the power function. <bookmark mark='a'/> Suppose that, from any "
            "initial wealth, a person turns down the bet of losing a hundred or gaining a hundred and ten. Then, if "
            "she maximizes expected utility with any increasing, concave utility function, she will turn down "
            "fifty-fifty bets of losing a thousand dollars or gaining any sum of money. <bookmark mark='b'/> His "
            "table: with a loss of four hundred, she refuses gains up to five hundred and fifty; six hundred, gains up "
            "to nine hundred and ninety; eight hundred, up to two thousand and ninety; a thousand or more, any gain at "
            "all. <bookmark mark='c'/> And weakening the premise barely helps. If she refuses the small bet only when "
            "her wealth is under three hundred thousand dollars, she still turns down losing a thousand against "
            "winning over seven hundred thousand."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(q, color=RISKY, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.5),
                      run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def moral(self):
        rows = VGroup(
            label(r"expected utility of \emph{wealth} cannot be risk averse over small stakes \\ without being "
                  r"absurdly risk averse over large ones", font_size=29, color=E.ACCENT),
            label(r"the small-stakes aversion is real: \ deductibles, \ the lab, \ refused bets", font_size=26),
            label(r"so it comes from something else: \ losses felt more than gains, \\ each bet judged on its own "
                  r"(``narrow framing''), \ not as a ripple in wealth", font_size=26, color=FAN),
            label(r"Rabin and Thaler (2001): \ ``beating at a dead parrot''; \ expected utility is ``an "
                  r"ex-hypothesis''", font_size=24, color=GREY_A),
            label(r"the same arithmetic warns any measurement: \\ a $\gamma$ read from small stakes says nothing about "
                  r"large ones", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "What follows? <bookmark mark='a'/> Expected utility over total wealth cannot explain risk aversion over "
            "small stakes without implying absurd aversion over large ones. <bookmark mark='b'/> And the small-stakes "
            "aversion is real: we saw it in deductibles, we'll see it in the laboratory. <bookmark mark='c'/> So it "
            "must come from something else. The leading explanation is that people feel losses more than gains, and "
            "judge each bet on its own, rather than as a tiny change in their lifetime wealth: what's called narrow "
            "framing. <bookmark mark='d'/> Rabin and Richard Thaler, the next year, said they felt like the "
            "customer in Monty Python's pet shop, beating at a dead parrot: expected utility, they concluded, is an "
            "ex-hypothesis. "
            "<bookmark mark='e'/> And there's a warning for measurement: a gamma read from choices over a few dollars "
            "says nothing about how someone will treat their pension."
        ) as vo:
            self.play(FadeIn(rows[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=E.ACCENT, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.15))
        self.clear_scene()
