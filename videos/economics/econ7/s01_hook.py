from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


def coin_row(n_tails: int, r: float = 0.34) -> VGroup:
    """One game: tails until the last toss, which is heads."""
    return VGroup(*[coin_glyph(r, "T", GREY_B) for _ in range(n_tails)], coin_glyph(r, "H", COINC)).arrange(
        RIGHT, buff=0.12)


class Hook(VoiceoverScene):
    def construct(self):
        self.game()
        self.expected()
        self.ask()
        self.million()
        self.bernoulli()
        self.question()
        self.title()
        self.objectives()
        self.advice()

    def game(self):
        s = load("stpete")
        head = label(r"St Petersburg, \ a game", font_size=38, color=COINC).to_edge(UP, buff=0.5)
        rule = VGroup(label(r"toss a coin until it lands heads", font_size=30),
                      label(r"heads on the first toss: \ \$1; \ on the second: \ \$2; \ on the third: \ \$4; \ "
                            r"and so on, \ doubling", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.2)
        rule.next_to(head, DOWN, buff=0.4)
        rows = VGroup()
        for i, k in enumerate(s["tosses"][:5]):
            prize = 2 ** (int(k) - 1)
            row = VGroup(label(rf"game {i + 1}", font_size=28, color=GREY_B), coin_row(int(k) - 1),
                         label(rf"\${prize}", font_size=40, color=COINC))
            row[1].next_to(row[0], RIGHT, buff=0.4)
            row[2].next_to(row[1], RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(rule, DOWN, buff=0.5)
        with self.voiceover(
            "Here is a game. <bookmark mark='a'/> I toss a coin until it lands heads. If it's heads on the first "
            "toss, I pay you one dollar. If the first head comes on the second toss, two dollars; on the third, "
            "four; and so on, the prize doubling with every tail. <bookmark mark='b'/> Most games end quickly. "
            "Heads at once: a dollar. Tails, tails, heads: four dollars. Now and then the tails run on, and the "
            "prize gets large."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            for row in rows:
                self.play(FadeIn(row[0]), LaggedStart(*[FadeIn(c, scale=0.6) for c in row[1]], lag_ratio=0.25),
                          FadeIn(row[2], shift=LEFT * 0.1), run_time=0.9)
        self.clear_scene()

    def expected(self):
        s = load("stpete")
        ks, prob, prize = s["ks"][:8], s["prob"][:8], s["prize"][:8]
        terms = VGroup()
        for k, p_, x in zip(ks, prob, prize):
            t = MathTex(rf"\tfrac{{1}}{{{int(round(1 / p_))}}}", r"\times", rf"\${int(x)}", font_size=34)
            t[2].set_color(COINC)
            terms.add(t)
        plus = [MathTex(r"+", font_size=34) for _ in range(len(terms) - 1)]
        line = VGroup()
        for i, t in enumerate(terms):
            line.add(t)
            if i < len(plus):
                line.add(plus[i])
        line.add(MathTex(r"+\;\cdots", font_size=34))
        line.arrange(RIGHT, buff=0.14).move_to(UP * 1.9)
        if line.width > 13.2:
            line.width = 13.2
        halves = VGroup(*[MathTex(r"0.50", font_size=30, color=COINC).next_to(t, DOWN, buff=0.35) for t in terms])
        total = MathTex(r"\text{expected prize} \;=\; 0.50 + 0.50 + 0.50 + \cdots \;=\; \infty", font_size=44,
                        color=COINC).move_to(DOWN * 0.3)
        ax = plane([0, 40], [0, 21], center=DOWN * 2.4, x_length=8.0, y_length=1.8, xticks=[0, 10, 20, 30, 40],
                   yticks=[0, 10, 20], xlabel=r"tosses allowed", ylabel=r"\$", font_size=16)
        n = np.arange(1, 41)
        ev = VMobject(stroke_color=COINC, stroke_width=3).set_points_as_corners([ax.ax.c2p(k, k / 2) for k in n])
        with self.voiceover(
            "What is the game worth, on average? <bookmark mark='a'/> Half the time it pays a dollar: that's worth "
            "fifty cents. A quarter of the time it pays two dollars: another fifty cents. An eighth of the time, "
            "four dollars: fifty cents again. <bookmark mark='b'/> Every possible ending adds fifty cents, and "
            "there's no last one. <bookmark mark='c'/> The expected prize is infinite. Allow the coin forty tosses "
            "and the average prize is twenty dollars; allow it forever, and no sum of money is the game's average "
            "value."
        ) as vo:
            self.play(FadeIn(line[:6]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h) for h in halves[:3]], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(line[6:]), LaggedStart(*[FadeIn(h) for h in halves[3:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Write(total), run_time=1.4)
            self.play(FadeIn(ax), Create(ev), run_time=2.0)
        self.clear_scene()

    def ask(self):
        q = label(r"What is the most you would pay to play it, once?", font_size=40, color=COINC).move_to(UP * 1.2)
        sub = label(r"its expected prize is infinite; \ name your price", font_size=28, color=GREY_A).next_to(
            q, DOWN, buff=0.35)
        ring = countdown().next_to(sub, DOWN, buff=0.6)
        with self.voiceover(
            "So what is the most you would pay to play it, once? Pause the film and name a price."
        ):
            self.play(FadeIn(q), FadeIn(sub))
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        note_ = label(r"hold on to it: \ we score it at the end", font_size=28, color=GREY_B).next_to(ring, DOWN,
                                                                                                     buff=0.4)
        self.play(FadeIn(note_))
        self.wait(1.0)
        self.clear_scene()

    def million(self):
        s = load("stpete")
        at, run = np.array(s["run_at"]), np.array(s["run"])
        ax = plane([0, 6], [0, 14], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.8, y_length=5.2,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 2, 4, 6, 8, 10, 12, 14],
                   xlabel=r"games played \ (log scale)", ylabel=r"average prize so far, \ \$", font_size=17,
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"))
        a = ax.ax
        curve = VMobject(stroke_color=COINC, stroke_width=3).set_points_as_corners(
            [a.c2p(np.log10(x), y) for x, y in zip(at, run) if y <= 14])
        guide = DashedVMobject(VMobject(stroke_color=GREY_B, stroke_width=2).set_points_as_corners(
            [a.c2p(np.log10(x), 0.5 * np.log2(x) + 1) for x in np.logspace(0, 6, 50)]), num_dashes=40)
        gl = label(r"about \ $\tfrac12\log_2 n + 1$", font_size=19, color=GREY_B).move_to(a.c2p(4.9, 5.6))
        side = VGroup(
            label(rf"{s['games']:,} simulated games".replace(",", "{,}"), font_size=26),
            label(rf"half of them pay \$1; \ {100 * s['share_le_4']:.1f}\% pay \$4 or less", font_size=23,
                  color=GREY_A),
            label(rf"the biggest prize: \ \${s['max_prize']:,.0f}".replace(",", "{,}"), font_size=23, color=COINC),
            label(r"the average never settles: \\ it creeps up for ever, \\ in jumps", font_size=25,
                  color=COINC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: a million games (seeded)", corner=DR, font_size=15)
        with self.voiceover(
            "Before you decide, watch a million games. <bookmark mark='a'/> Half of them pay a dollar. Seven in "
            "eight pay four dollars or less. <bookmark mark='b'/> But every so often a long run of tails pays a "
            "fortune: the biggest prize in this million was over half a million dollars. <bookmark mark='c'/> So "
            "the average prize never settles down, the way averages are supposed to. It creeps upward for ever, in "
            "jumps, roughly half a dollar for every doubling of the number of games. After a million games it "
            "stands at about eleven dollars."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curve), run_time=5.0, rate_func=linear)
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(guide), FadeIn(gl), FadeIn(side[3]))
        self.clear_scene()

    def bernoulli(self):
        s = load("stpete")
        b = tables.BERNOULLI_1738.data
        c1 = history_card(1713, r"Nicolaus Bernoulli \ poses it", r"in a letter to Montmort: \ what should a "
                          r"player pay?", color=GREY_A, width=4.1, font_size=21)
        c2 = history_card(1728, r"Gabriel Cramer \ answers", r"value money by its square root: \ the game is worth "
                          r"about 2.9", color=LATER, width=4.1, font_size=21)
        c3 = history_card(1738, r"Daniel Bernoulli \ publishes", r"in St Petersburg: \ value money by the "
                          r"logarithm of your wealth", color=COINC, width=4.1, font_size=21)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.45)
        idea = label(r"a gain of \$1 means less to the rich than to the poor: \ \emph{diminishing marginal utility}",
                     font_size=27, color=UTIL).next_to(cards, DOWN, buff=0.45)
        n = s["named"]
        prices = VGroup(
            label(r"Bernoulli's price for the game:", font_size=27),
            label(rf"with \$100 to your name: \ \${n['100']['log']:.2f}", font_size=26, color=COINC),
            label(rf"with \$1{{,}}000: \ \${n['1000']['log']:.2f}", font_size=26, color=COINC),
            label(rf"with \$1 million: \ \${n['1e+06']['log']:.2f}", font_size=26, color=COINC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(idea, DOWN, buff=0.4).shift(LEFT * 2.6)
        quote = quote_card(b["twenty_ducats"], r"Daniel Bernoulli (1738), as quoted by Hayden and Platt (2009)",
                           width=5.2, font_size=21, color=COINC).next_to(prices, RIGHT, buff=0.6)
        tag = published_tag(r"the Stanford Encyclopedia of Philosophy, ``The St.\ Petersburg Paradox''", corner=DR,
                            font_size=13)
        head = label(r"the St Petersburg paradox, \ 1713--1738", font_size=34, color=COINC).to_edge(UP, buff=0.35)
        cards.next_to(head, DOWN, buff=0.35)
        idea.next_to(cards, DOWN, buff=0.4)
        prices.next_to(idea, DOWN, buff=0.35).shift(LEFT * 2.6)
        quote.next_to(prices, RIGHT, buff=0.6)
        with self.voiceover(
            "This is the St Petersburg game, and it has a history. <bookmark mark='a'/> Nicolaus Bernoulli posed it in "
            "1713, in a letter to the French mathematician Pierre de Montmort. <bookmark mark='b'/> Fifteen years "
            "later the Swiss mathematician Gabriel Cramer suggested the answer: people don't value money by its "
            "amount but by something like its square root, and on that reckoning the game is worth about two "
            "dollars ninety. <bookmark mark='c'/> And in 1738 Nicolaus's cousin Daniel published the solution that "
            "stuck, in the journal of the academy in St Petersburg. <bookmark mark='d'/> A gain of one ducat, he "
            "argued, means less to a rich man than to a poor one; value a sum by the logarithm of your wealth. "
            "That was the first utility function. <bookmark mark='e'/> On Bernoulli's rule, someone with a hundred "
            "dollars would pay four thirty-six to play; with a thousand dollars, five ninety-seven; a millionaire, "
            "ten ninety-four. Small, finite prices, rising with wealth. Hold on to your own price: at the end of "
            "this part we'll see what people actually pay."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(c3, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(idea))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in prices], lag_ratio=0.4),
                      FadeIn(quote), run_time=3)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.7)
        rows = VGroup(
            label(r"how does a pay-off next year compare with one today?", font_size=30, color=TODAY),
            label(r"how does a gamble compare with a sure thing?", font_size=30, color=RISKY),
            label(r"and do people choose the way the theory says?", font_size=30, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Every real choice has two things the last two parts left out: time and risk. So this part asks: how do "
            "people choose when the pay-off comes later, or may not come at all? <bookmark mark='a'/> How does a "
            "pay-off next year compare with one today? <bookmark mark='b'/> How does a gamble compare with a sure "
            "thing? <bookmark mark='c'/> And when we watch people choose, do they do what the theory says?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = VGroup(coin_glyph(0.55, "H"), coin_glyph(0.55, "T", GREY_B)).arrange(RIGHT, buff=0.3)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 7 \ $\cdot$ \ Time and Risk", font_size=34, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part seven: time and risk."):
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in logo], lag_ratio=0.4), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act II \ $\cdot$ \ Choosing", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"Fisher's two periods: \ the interest rate as a price, \ and the Euler equation",
            r"discounting, \ lotteries, \ and expected utility drawn in a triangle",
            r"risk aversion in numbers: \ certainty equivalents, \ insurance, \ a risky asset",
            r"where expected utility breaks: \ Allais, \ Ellsberg, \ Rabin, \ present bias",
            r"how risk and time preferences are measured, \ and what the estimates say",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Two, on choosing. <bookmark mark='a'/> We'll start with Irving Fisher's two "
            "periods, where the interest rate is a price and one equation governs saving. <bookmark mark='b'/> Then "
            "discounting, lotteries, and the theory of expected utility, which we'll draw in a triangle. "
            "<bookmark mark='c'/> We'll put numbers on risk aversion: what a gamble is worth for sure, how much "
            "insurance to buy, how much to put in a risky asset. <bookmark mark='d'/> We'll see where the theory "
            "breaks, in four famous places. <bookmark mark='e'/> And how economists measure these preferences, and "
            "what their measurements say."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def advice(self):
        box = RoundedRectangle(width=10.6, height=3.0, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2,
                               fill_color=GREY_E, fill_opacity=0.5)
        t = VGroup(label(r"Not financial advice", font_size=38, color=WHITE),
                   label(r"this part is about how choices under time and risk are modelled and measured; \\ "
                         r"its insurance, pension and investment examples are illustrations, \\ not recommendations "
                         r"for anyone's money", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35).move_to(box)
        with self.voiceover(
            "One card before we start. This part is about how choices over time and risk are modelled and measured. "
            "Its examples of insurance, pensions and investment are illustrations, not advice about anyone's money."
        ):
            self.play(FadeIn(box), FadeIn(t))
        self.wait(1.0)
        self.clear_scene()
