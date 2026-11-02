from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load


class MarketMaker(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.book(load("mm"))
        self.firms()

    def card(self):
        c = chapter_card(4, r"The market maker's book", r"How do you quote a price without knowing the answer?", part=PART)
        with self.voiceover("Chapter four. The market maker's book."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def game(self):
        q = desk_question(r"Make me a market on the roll of a die. \ldots Now I tell you the roll is even. Make me a new "
                          r"market.", width=10.6, font_size=28).to_edge(UP, buff=0.6)
        rows = [cmath(r"\mathbb{E}[X]", r"=", r"3.5\quad\Rightarrow\quad 3.3\ \text{bid},\ 3.7\ \text{ask}", font_size=36,
                      colors={r"\mathbb{E}[X]": OPT}),
                cmath(r"\mathbb{E}[X \mid \text{even}]", r"=", r"4\quad\Rightarrow\quad 3.8\ /\ 4.2", font_size=36,
                      colors={r"\mathbb{E}[X \mid \text{even}]": ALT})]
        whys = [why(r"quote around fair value, wide enough to be paid for the risk: the spread is the market maker's "
                    r"income and its insurance"),
                why(r"new information moves the fair value; and the person asking may know more than you, so after a "
                    r"trade, fair value moves against you: adverse selection (Glosten and Milgrom 1985)")]
        step = ladder(self, rows, whys, keep=2, top=0.9, x=-0.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "The classic market-making interview game. Make me a market on the roll of a die. The expected roll is "
            "three and a half, so you quote around it: buy at three point three, sell at three point seven. The "
            "spread is your income, and your protection. <bookmark mark='a'/> Then the interviewer says: the roll is "
            "even. Your fair value jumps to four, and your market with it. The lesson is the one that rules every "
            "options desk: the person trading with you may know something, so after each trade the fair value tends "
            "to move against you. Lawrence Glosten and Paul Milgrom called it adverse selection in 1985."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def book(self, m):
        a, b = m["no skew"], m["skewed"]
        ia, ib = np.asarray(a["inventory"]), np.asarray(b["inventory"])
        x = np.arange(len(ia)) * 5
        lim = max(np.abs(ia).max(), np.abs(ib).max()) + 2
        g = axes([0, x[-1]], [-lim, lim], x_length=7.2, y_length=4.2, xlabel=r"client requests",
                 ylabel=r"inventory, in units of vega", xticks=[0, 500, 1000, 1500, 2000], yticks=[-40, -20, 0, 20, 40],
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        la = curve(ax, x, ia, THETA, stroke_width=2.5)
        lb = curve(ax, x, ib, GAMMA, stroke_width=3)
        leg = legend([(THETA, r"quotes fixed around fair value"), (GAMMA, r"quotes skewed against inventory")],
                     font_size=19).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            MathTex(r"\text{mid} = \sigma_{\text{fair}} - k \cdot \text{vega inventory}", font_size=30, color=VEGA),
            wrapped_label(r"long vega already? quote lower, so clients buy from you and stop selling to you (Avellaneda "
                          r"and Stoikov 2008, in volatility units)", 4.4, 20, GREY_A),
            MathTex(rf"\text{{largest inventory: }} {a['max_abs']:.0f} \to {b['max_abs']:.0f}", font_size=30, color=GAMMA),
            MathTex(rf"\text{{spread earned: }} {a['spread_pnl']:.1f} \to {b['spread_pnl']:.1f}", font_size=30),
            wrapped_label(r"a little income given up for a book that stays small: what is left is hedged in the "
                          r"underlying (delta) and with other options (vega)", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"a toy: 2{,}000 random client requests, the same for both books")
        with self.voiceover(
            "An options market maker plays this game all day, in volatility. Clients arrive at random, some to buy "
            "volatility and some to sell. A desk that quotes fixed around fair value lets its inventory wander, "
            f"here as far as {a['max_abs']:.0f} units of vega. <bookmark mark='a'/> The fix is to lean the quotes "
            "against the inventory: long vega already, quote a little lower, so that clients buy from you and stop "
            "selling to you. Marco Avellaneda and Sasha Stoikov wrote down the optimal version in 2008. "
            f"<bookmark mark='b'/> The same clients, the same day: the largest inventory falls to {b['max_abs']:.0f}, "
            "for a small loss of spread income. What remains is hedged, delta with the underlying, vega with other "
            "options."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(la), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(leg[1]), FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def firms(self):
        cards = VGroup(
            firm_card(r"Susquehanna (SIG)", r"Founded in 1987, months before Black Monday, as an options market maker. "
                      r"Its graduate training, by its own job postings, teaches game theory and decision science, with "
                      r"classes in poker.", width=4.3, font_size=24),
            firm_card(r"Optiver and IMC", r"Amsterdam market makers founded in 1986 and 1989, on the European options "
                      r"exchange floors; now electronic, quoting options and ETFs worldwide.", width=4.3, font_size=24),
            firm_card(r"Jane Street", r"Founded around the turn of the millennium; a market maker in ETFs, bonds and "
                      r"options across the world's exchanges, and a large trader in India's index options (chapter 6).", width=4.3,
                      font_size=24),
        ).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        with self.voiceover(
            "A few of the firms that do this for a living, from the public record. Susquehanna began in 1987, months "
            "before the crash of Black Monday, as an options market maker; its graduate training, by its own job "
            "postings, teaches game theory and decision science, and includes classes in poker. <bookmark mark='a'/> "
            "Optiver and IMC began on the Amsterdam options floor in 1986 and 1989, and now quote electronically "
            "across the world. <bookmark mark='b'/> And Jane Street, founded around the turn of the millennium, makes "
            "markets in exchange-traded funds, bonds and options, and was a large trader in India's index options, "
            "which chapter six returns to."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
