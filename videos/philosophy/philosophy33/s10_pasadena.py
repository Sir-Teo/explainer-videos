from __future__ import annotations

from fractions import Fraction

from videos.philosophy.philosophy33.common import *  # noqa: F403


def partial_sums(order: str, n: int) -> list[float]:
    """Partial sums of 1 - 1/2 + 1/3 - ... taken in the natural order, or two positive terms to one negative."""
    out, s = [], 0.0
    if order == "natural":
        for k in range(1, n + 1):
            s += (-1) ** (k - 1) / k
            out.append(s)
    else:
        pos, neg = 1, 2
        while len(out) < n:
            for _ in range(2):
                s += 1 / pos
                pos += 2
                out.append(s)
            s -= 1 / neg
            neg += 2
            out.append(s)
    return out[:n]


class Pasadena(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Pasadena", r"What is a game worth when its expectation depends on the order of "
                                            r"addition?", lit=(2004,), part=PART)
        with self.voiceover("Chapter nine. Pasadena."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.rearranged()
        self.responses()

    def game(self):
        head = label(r"The Pasadena game \ (Nover and H\'ajek, \ 2004)", font_size=30, color=CONN).to_edge(UP,
                                                                                                          buff=0.3)
        hd = [r"\text{first heads on toss } n", r"\text{probability}", r"\text{payoff}", r"\text{contribution}"]
        cells = []
        for n in range(1, 6):
            fr = Fraction(2 ** n, n) * (1 if n % 2 else -1)
            pay = f"{fr.numerator}" if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"
            cells.append([label(str(n), font_size=20), MathTex(rf"1/{2 ** n}", font_size=26, color=RISK),
                          MathTex(pay, font_size=26, color=OK if n % 2 else BAD),
                          MathTex(rf"{'+' if n % 2 else '-'}\tfrac{{1}}{{{n}}}", font_size=28, color=GOAL)])
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.2, 2.2, 2.6], cell_h=0.6, font_size=19).move_to([0, 0.5, 0])
        f = MathTex(r"\mathbb{E} \;=\; 1 - \tfrac{1}{2} + \tfrac{1}{3} - \tfrac{1}{4} + \tfrac{1}{5} - \cdots",
                    font_size=36, color=PREF).to_edge(DOWN, buff=0.9)
        note = label(r"odd tosses: \ you win $2^n/n$; \ even tosses: \ you pay it", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 2004 Harris Nover and Alan Hájek designed a game to break expected utility in a new way. "
            "<bookmark mark='a'/>Toss a coin until it lands heads. If that happens on toss n, and n is odd, you win "
            "two to the n divided by n dollars; if n is even, you pay that much. <bookmark mark='b'/>Two dollars, "
            "then minus two, then eight thirds, then minus four, then six point four. "
            "<bookmark mark='c'/>The contributions to the expectation are one, minus a half, a third, minus a "
            "quarter: the alternating harmonic series, which adds up to the natural logarithm of two, about point "
            "six nine. So the game is worth sixty nine cents. Or is it?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), FadeIn(note))
            vo.wait_until("a")
            for r in range(2):
                self.play(*[FadeIn(c) for c in grid.cell[r][:3]], run_time=0.5)
            vo.wait_until("b")
            for r in range(2, 5):
                self.play(*[FadeIn(c) for c in grid.cell[r][:3]], run_time=0.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][3]) for r in range(5)], lag_ratio=0.2))
            self.play(Write(f))
        self.clear_scene()

    def rearranged(self):
        d = load("pasadena")
        head = label(r"The same terms, \ added in another order", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["natural"] == 0.69314 and d["two_one"] == 1.03972 and d["three_halves_ln2"] == 1.03972
        n = 60
        nat, two = partial_sums("natural", n), partial_sums("two_one", n)
        ax = Axes(x_range=[0, n, 10], y_range=[0.4, 1.4, 0.2], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True},
                  y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.0, -0.6, 0])
        xl = label(r"terms added", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        c1 = VMobject(color=PREF, stroke_width=2.5).set_points_as_corners([ax.c2p(k + 1, s) for k, s in
                                                                           enumerate(nat)])
        c2 = VMobject(color=RISK, stroke_width=2.5).set_points_as_corners([ax.c2p(k + 1, s) for k, s in
                                                                           enumerate(two)])
        l1 = DashedLine(ax.c2p(0, math.log(2)), ax.c2p(n, math.log(2)), color=PREF, stroke_width=1.5)
        l2 = DashedLine(ax.c2p(0, 1.5 * math.log(2)), ax.c2p(n, 1.5 * math.log(2)), color=RISK, stroke_width=1.5)
        side = stack([(r"in order: \ $\to \ln 2 = 0.69314$", PREF),
                      (r"two wins, \ then one loss: \ $\to \tfrac{3}{2}\ln 2 = 1.03972$", RISK),
                      (r"Riemann \ (1854): \ a conditionally convergent series can be rearranged to any sum", GOAL),
                      (r"the coin does not say in which order to add", BAD)], font_size=18, aligned_edge=LEFT,
                     width=4.4, buff=0.3).move_to([4.4, -0.3, 0])
        f = MathTex(r"\sum |\text{contribution}| \;=\; 1 + \tfrac12 + \tfrac13 + \cdots \;=\; \infty", font_size=28,
                    color=GREY_A).next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            "The trouble is the order. <bookmark mark='a'/>Add the contributions in the order of the tosses, and "
            "the running total settles on the logarithm of two. The Reasoner's two hundred thousand terms give "
            "point six nine three one four. <bookmark mark='b'/>Now add the same terms in a different order: two "
            "positive terms, then one negative. Every term is still used exactly once. The total now settles on "
            "three halves of the logarithm of two, one point zero three nine seven. <bookmark mark='c'/>This is "
            "Riemann's rearrangement theorem: because the absolute values add up to infinity, the series can be "
            "rearranged to converge to any number at all, or to diverge. <bookmark mark='d'/>Nothing in the game "
            "picks the order. The outcomes are just outcomes; listing them by toss is our choice. So the "
            "expectation of the Pasadena game is undefined, and expected utility theory says nothing about whether "
            "to play it for a dollar, or for a cent."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(c1), Create(l1), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(c2), Create(l2), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(f), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def responses(self):
        head = label(r"Responses", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"weak expectation", r"Easwaran \ (2008): \ value the game by what the average of many plays tends "
                                      r"to, \ in probability: \ $\ln 2$", PREF),
                (r"relative expectation", r"Colyvan \ (2006): \ compare two games by the expectation of their "
                                          r"difference, \ which can be well defined", CAUSE),
                (r"bounded utility", r"if utility is bounded, \ no such game can exist; \ the price is that "
                                     r"some large stakes stop mattering", RISK),
                (r"the lesson", r"expected utility needs the expectation to exist; \ with infinitely many outcomes it "
                                r"may not", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Philosophers have offered repairs. <bookmark mark='a'/>Kenny Easwaran proposed the weak expectation: the "
            "value the average of many plays tends to, in probability. For the Pasadena game it is the logarithm of "
            "two. <bookmark mark='b'/>Mark Colyvan proposed comparing two games by the expectation of their "
            "difference, which can exist when neither game's expectation does. <bookmark mark='c'/>Or utility is "
            "bounded, as Menger's game already suggested, and such games cannot be built from utilities at all; the "
            "price is that some very large stakes stop mattering. <bookmark mark='d'/>The lesson is general. "
            "Expected utility theory assumes the expectation exists. With infinitely many possible outcomes, as in "
            "Pascal's wager of Part 23, it may not, and the theory falls silent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
