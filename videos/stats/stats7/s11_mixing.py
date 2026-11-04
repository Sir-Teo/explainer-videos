from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403

CARD_COLS = [interpolate_color(ManimColor(S.EST), ManimColor(S.POST), k / 9) for k in range(10)]


def card(k, w=0.42, h=0.62):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=BLACK, stroke_width=1.5,
                                   fill_color=CARD_COLS[k], fill_opacity=1), MathTex(str(k + 1), font_size=20, color=BLACK))


class Mixing(VoiceoverScene):
    def construct(self):
        self.card_()
        self.riffle()
        self.rising()
        self.seven()
        self.check()
        self.cutoff()

    def card_(self):
        c = chapter_card(10, r"Mixing: \ seven shuffles", r"How long until a chain forgets where it started?", lit=(1992,), part=PART)
        with self.voiceover("Chapter ten. Mixing, and seven shuffles."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def riffle(self):
        rng = np.random.Generator(np.random.PCG64(52))
        deck = list(range(10))
        cards = {k: card(k) for k in deck}
        y0 = 1.6
        for i, k in enumerate(deck):
            cards[k].move_to([-2.3 + 0.5 * i, y0, 0])
        rows = fit_rows(VGroup(
            label(r"1. \ cut: \ the top packet has $\mathrm{Binomial}(n, \tfrac12)$ cards", font_size=24),
            label(r"2. \ riffle: \ drop the next card from a packet with chance $\propto$ its size", font_size=24),
            label(r"the Gilbert--Shannon--Reeds model (1955, 1981): \ a Markov chain on the $n!$ orderings", font_size=22,
                  color=GREY_A),
        ), 12.6, 0.25, [0, -2.4, 0])
        with self.voiceover(
            "How many times must you shuffle a deck of cards before it's truly mixed? This is a question about a "
            "Markov chain whose states are the orderings of the deck. <bookmark mark='a'/> Here's a ten-card deck "
            "and the standard model of a riffle shuffle. First, cut the deck: the size of the top packet is binomial, "
            "so usually near the middle. <bookmark mark='b'/> Then riffle: let cards fall one at a time from the two "
            "packets, each time choosing a packet with probability proportional to how many cards it still holds. "
            "<bookmark mark='c'/> This model, due to Edgar Gilbert and Claude Shannon and independently Jim Reeds, "
            "matches how real people shuffle surprisingly well. Watch three shuffles."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(cards[k]) for k in deck], lag_ratio=0.05))
            for s in range(3):
                c = int(rng.binomial(10, 0.5))
                L, R = deck[:c], deck[c:]
                if s == 0:
                    vo.wait_until("a")
                    self.play(FadeIn(rows[0]))
                self.play(*[cards[k].animate.move_to([-3.6 + 0.5 * i, y0 - 1.0, 0]) for i, k in enumerate(L)],
                          *[cards[k].animate.move_to([0.6 + 0.5 * i, y0 - 1.0, 0]) for i, k in enumerate(R)], run_time=0.8)
                if s == 0:
                    vo.wait_until("b")
                    self.play(FadeIn(rows[1]))
                new = []
                while L or R:
                    if rng.random() < len(L) / (len(L) + len(R)):
                        new.append(L.pop(0))
                    else:
                        new.append(R.pop(0))
                self.play(*[cards[k].animate.move_to([-2.3 + 0.5 * i, y0, 0]) for i, k in enumerate(new)], run_time=1.0)
                deck = new
                if s == 0:
                    vo.wait_until("c")
                    self.play(FadeIn(rows[2]))
        self.clear_scene()

    def rising(self):
        rows = [
            cmath(r"P_k(\sigma)", r"=", r"\binom{2^k + n - r(\sigma)}{n} \Big/ 2^{nk}", font_size=32),
            cmath(r"\|P_k - U\|_{\mathrm{TV}}", r"=", r"\frac12 \sum_{r = 1}^{n} A_{n,r}\, \Big|\binom{2^k + n - r}{n}2^{-nk} - \frac{1}{n!}\Big|",
                  font_size=30),
        ]
        rows[1][2].set_color(S.ACCENT)
        whys = [why(r"after $k$ shuffles, \ a deck's chance depends only on $r(\sigma)$, \ its number of rising sequences"),
                why(r"$A_{n,r}$: \ how many orderings have $r$ rising sequences (Eulerian numbers): \ 52 terms, \ not $52!$")]
        ex = fit_rows(VGroup(
            label(r"a rising sequence: \ cards $i, i+1, i+2, \dots$ appearing in order, \ interleaved with others", font_size=22,
                  color=GREY_A),
            label(r"one riffle shuffle makes at most 2; \ $k$ shuffles at most $2^k$", font_size=22, color=GREY_A),
            label(r"total variation: \ the largest difference, over any event, \ between the deck's law and the uniform", font_size=22,
                  color=GREY_A),
        ), 12.6, 0.22, [0, -2.2, 0])
        with self.voiceover(
            "How close is the deck to uniform after k shuffles? There are fifty-two factorial orderings, about eight "
            "times ten to the sixty-seven, so we can't list them. Dave Bayer and Persi Diaconis found a way around "
            "it in 1992. <bookmark mark='a'/> After k riffle shuffles, the chance of any particular ordering depends "
            "only on its number of rising sequences: runs of consecutive cards that still appear in their original "
            "order. A single shuffle creates at most two; k shuffles at most two to the k. <bookmark mark='b'/> So the "
            "total variation distance to the uniform, the largest error in the probability of any event, is a sum "
            "of only fifty-two terms, weighted by the Eulerian numbers that count orderings with each number of "
            "rising sequences. We can compute it exactly."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.4, buff=1.3, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            self.play(FadeIn(ex[:2]))
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(ex[2]))
        self.clear_scene()

    def seven(self):
        d = load("shuffle")
        tv = np.asarray(d["52"])[:12]
        A = axes([0.4, 12.6], [0, 1.08], x_length=8.0, y_length=4.4, xlabel=r"riffle shuffles $k$", ylabel=r"total variation to uniform",
                 xticks=list(range(1, 13)), yticks=[0, 0.25, 0.5, 0.75, 1], center=[-1.4, -0.4, 0])
        ax = A.ax
        bs = bars(ax, np.arange(1, 13), tv, S.EST, width=0.6)
        for k in (6,):
            bs[k].set_fill(S.ACCENT, opacity=0.95)
        vals = VGroup(*[MathTex(f"{v:.3f}", font_size=18, color=GREY_A).next_to(bs[i], UP, buff=0.06) for i, v in enumerate(tv)])
        hc = history_card(1992, r"Bayer \& Diaconis, \ ``Trailing the dovetail shuffle to its lair''",
                          r"\emph{Annals of Applied Probability}: \ seven riffle shuffles, \ and the newspapers noticed",
                          color=S.MUSEUM, width=4.6, font_size=20).move_to([4.6, 2.1, 0])
        with self.voiceover(
            "Here's the answer for fifty-two cards. <bookmark mark='a'/> After one, two, three, even four shuffles the "
            "distance is essentially one: the deck is as far from random as it can be, and a clever gambler could "
            "exploit it. <bookmark mark='b'/> At five it starts to drop, point nine two; at six, point six one. "
            "<bookmark mark='c'/> At seven, a third, and from there it halves with every shuffle. "
            "<bookmark mark='d'/> Bayer and Diaconis's verdict, which made the newspapers: seven shuffles are needed, "
            "and more are not worth much."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs[:4]], lag_ratio=0.2), FadeIn(vals[:4]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bs[4], DOWN), GrowFromEdge(bs[5], DOWN), FadeIn(vals[4:6]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs[6:]], lag_ratio=0.15), FadeIn(vals[6:]))
            vo.wait_until("d")
            self.play(FadeIn(hc))
        self.clear_scene()

    def check(self):
        d = load("shuffle")
        ex, sim = np.asarray(d["5"])[:8], np.asarray(d["sim5"])
        A = axes([0.4, 8.6], [0, 0.85], x_length=7.0, y_length=4.2, xlabel=r"riffle shuffles $k$, \ a 5-card deck",
                 ylabel=r"total variation", xticks=list(range(1, 9)), yticks=[0, 0.25, 0.5, 0.75], center=[-2.0, -0.4, 0])
        ax = A.ax
        b1 = bars(ax, np.arange(1, 9) - 0.17, ex, EXACT, width=0.3)
        b2 = bars(ax, np.arange(1, 9) + 0.17, sim, GOOD, width=0.3)
        leg = legend([(EXACT, r"exact (Bayer--Diaconis)"), (GOOD, r"simulated: \ 60,000 decks")], font_size=22).move_to([4.2, 1.8, 0])
        rows = fit_rows(VGroup(label(r"agreement until the simulation's own noise floor, \ about 0.02", font_size=24),
                               label(r"120 orderings, \ 60,000 decks: \ 500 per ordering", font_size=22, color=GREY_A),
                               label(r"an exact formula and a simulation: \ each checks the other", font_size=24, color=S.ACCENT)),
                        5.2, 0.28, [4.2, -0.4, 0])
        with self.voiceover(
            "Can we trust the formula? Check it by simulation. <bookmark mark='a'/> With five cards there are only a "
            "hundred and twenty orderings, so we can shuffle sixty thousand decks with our generator and count. "
            "<bookmark mark='b'/> The simulated distances track the exact ones, until they reach the simulation's own "
            "noise floor, about two percent: with five hundred decks per ordering, the counts themselves wobble by "
            "that much. An exact answer and a simulation, each checking the other: that's the habit this part is "
            "trying to build."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(leg[1]), FadeIn(rows))
        self.clear_scene()

    def cutoff(self):
        rows = fit_rows(VGroup(
            label(r"the cutoff phenomenon: \ distance $\approx 1$, \ then a sudden drop near $\tfrac32 \log_2 n$ shuffles", font_size=26),
            MathTex(r"n = 52:\quad \tfrac32\log_2 52 \approx 8.6;\ \ \text{the drop starts at 5, and is a third by 7}", font_size=28,
                    color=S.ACCENT),
            label(r"other shuffles are far slower: \ overhand shuffling needs thousands (order $n^2 \log n$)", font_size=24,
                  color=GREY_A),
            label(r"for MCMC (chapter 11, \ Part 27): \ how long before a chain has forgotten its start?", font_size=26, color=CHAIN),
            label(r"the answer, \ like the deck's, \ is a property of the chain, \ not of patience", font_size=24, color=GREY_A),
        ), 12.6, 0.35, [0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The shape of that curve has a name: the cutoff phenomenon. The distance stays near one, "
            "then falls off a cliff, around one and a half times the base-two log of the number of cards. "
            "<bookmark mark='b'/> For fifty-two cards the drop begins at five and is a third by seven. "
            "<bookmark mark='c'/> Other ways of shuffling are much slower: the overhand shuffle, sliding small packets "
            "from hand to hand, needs thousands. <bookmark mark='d'/> The same question, how long until a chain has "
            "forgotten where it started, is the central practical question of Markov chain Monte Carlo, coming next "
            "and in Part 27. <bookmark mark='e'/> And the answer, like the deck's, depends on the chain."
        ) as vo:
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
