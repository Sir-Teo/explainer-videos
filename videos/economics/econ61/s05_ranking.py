from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Ranking(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Search and ranking", r"How much is the top of the page worth, \ and to whom?",
             "Chapter four. Search and ranking.", lit={2017: r"Google Shopping", 2018: r"Ursu"},
             scale=("person", "market"), horizon=("a day",))
        self.position()
        self.sponsored()
        self.steering()

    def position(self):
        R = load("ranking")
        ex, cl = np.array(R["examine"]), np.array(R["clicks"])
        n = len(ex)
        ax = plane([0.4, n + 0.6], [0, 1.1], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=list(range(1, n + 1)), yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"position on the page",
                   ylabel=r"per search", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        b_cl = bars(ax, np.arange(1, n + 1) - 0.18, cl, [SELL] * n, width=0.34)
        b_ex = bars(ax, np.arange(1, n + 1) + 0.18, ex, [PLAT] * n, width=0.34)
        side = VGroup(
            label(r"green: \ clicks on each position, \ as logged", font_size=19, color=SELL),
            label(rf"the top result gets {cl[0] / cl[4]:.1f} times the fifth's clicks", font_size=19, color=SELL),
            label(r"but the top result is also the most relevant", font_size=19, color=WHITE),
            label(r"purple: \ the chance a shopper looks at each position at all", font_size=19, color=PLAT),
            label(rf"position alone: \ top {ex[0] / ex[4]:.1f} times the fifth", font_size=21, color=PLAT),
            label(r"randomizing the order separates the two", font_size=19, color=TEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ a position-based click model; \ agora.platform.ranking", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Every marketplace is also a search engine, and its first design decision is the order of the "
            "results. <bookmark mark='a'/> Here are the Island marketplace's logged clicks on each position of a "
            f"results page. <bookmark mark='b'/> The top result gets {cl[0] / cl[4]:.1f} times as many clicks as "
            "the fifth. <bookmark mark='c'/> But that mixes two things: the top result is at the top, and it is "
            "also the result the algorithm thought most relevant. <bookmark mark='d'/> What the platform needs to "
            "know is the effect of position alone: the chance that a shopper looks at each slot at all. <bookmark "
            f"mark='e'/> On the Island, position alone gives the top slot {ex[0] / ex[4]:.1f} times the fifth's "
            "attention; the rest of the logged gap is relevance. <bookmark mark='f'/> Platforms learn this by "
            "randomizing the order for a small share of searches. Raluca Ursu did it with a travel site's hotel "
            "rankings, randomized: position changed which hotels people looked at, and much less which they booked "
            "once they had looked."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b_cl], lag_ratio=0.08), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b_ex], lag_ratio=0.08), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def sponsored(self):
        R = load("ranking")
        rel = np.array(R["relevance"])
        n = len(rel)
        rows = VGroup()
        for k in range(n):
            bar = Rectangle(width=4.2 * rel[k], height=0.3, stroke_width=0, fill_color=SELL, fill_opacity=0.85)
            num = label(rf"{k + 1}", font_size=17, color=GREY_A)
            rows.add(VGroup(num, bar))
        for k, r_ in enumerate(rows):
            r_[0].move_to([-6.2, 2.4 - k * 0.5, 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.3)
        head = label(r"relevance of the listing in each position", font_size=18, color=GREY_A).next_to(
            rows, UP, buff=0.25).align_to(rows, LEFT)
        spon = label(r"sponsored", font_size=15, color=AD)
        side = VGroup(
            label(r"the best page: \ listings in order of relevance", font_size=19, color=SELL),
            label(r"a seller pays for the top slot: \ its listing, \ sixth by relevance, \ moves up", font_size=19,
                  color=AD),
            label(rf"clicks per search: \ {R['total']:.2f} $\to$ {R['total_sponsored']:.2f}", font_size=20,
                  color=WHITE),
            label(rf"relevance of what is clicked: \ {R['quality']:.3f} $\to$ {R['quality_sponsored']:.3f}",
                  font_size=20, color=WHITE),
            label(r"the platform earns the ad's price, \\ and pays for it in its shoppers' attention", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.45)
        tag = island_tag(r"the Island: \ agora.platform.ranking", corner=DL, font_size=12)
        with self.voiceover(
            "Now sell the top of the page. <bookmark mark='a'/> Here is the page in order of relevance, the best "
            "the shopper could see. <bookmark mark='b'/> A seller whose listing is sixth by relevance pays for the "
            "top slot, and the two listings swap. <bookmark mark='c'/> Shoppers now look first at a worse match: "
            f"clicks per search fall from {R['total']:.2f} to {R['total_sponsored']:.2f}, <bookmark mark='d'/> and "
            f"the relevance of what they click falls from {R['quality']:.3f} to {R['quality_sponsored']:.3f}. "
            "<bookmark mark='e'/> The platform earns the ad's price, and pays for it in its shoppers' attention "
            "and trust. How many sponsored slots, and how far up, is a trade-off the platform's economists "
            "measure with experiments, because the cost shows up only slowly, in shoppers who come back less."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head), FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            a, b = rows[0][1], rows[5][1]
            pa, pb = a.get_left().copy(), b.get_left().copy()
            spon.next_to(rows[0][0], LEFT, buff=0.2)
            self.play(a.animate.move_to(pb, aligned_edge=LEFT), b.animate.move_to(pa, aligned_edge=LEFT),
                      FadeIn(spon), FadeIn(side[1]), run_time=1.4)
            self.play(b.animate.set_fill(AD))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def steering(self):
        cards = point_cards([
            (r"self-preferencing", r"a platform that sells its own products can rank them first: \ Part 44's worry, "
             r"now a question of measurement", PLAT),
            (r"Google Shopping, \ 2017", r"the European Commission fines Google 2.42 billion euros for "
             r"favouring its own comparison shopping in its results; \ upheld by the EU's Court of Justice in 2024",
             SURGE),
            (r"what the economist measures", r"how much of the ranking is relevance and how much is ownership, \ "
             r"and what shoppers lose", TEST),
            (r"the remedy's problem", r"a rule against favouring yourself needs a definition of the neutral "
             r"ranking, \ and there is none", GREY_A),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"when the ranker also sells", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"European Commission, \ case AT.39740 (2017); \ Court of Justice, \ C-48/22 P (2024)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "And when the platform that ranks also sells? <bookmark mark='a'/> It can put its own products first. "
            "That was Part forty-four's worry about vertical integration; here it becomes a question of "
            "measurement. <bookmark mark='b'/> In 2017 the European Commission fined Google two point four two "
            "billion euros for favouring its own comparison shopping service in its search results, a decision "
            "the EU's Court of Justice upheld in 2024. <bookmark mark='c'/> The economist's job in such a case is "
            "to measure how much of the ranking is relevance and how much is ownership, and what shoppers lose "
            "by it. <bookmark mark='d'/> And the remedy has a problem of its own: a rule against favouring "
            "yourself needs a definition of the neutral ranking, and there is no such thing, since every ranking "
            "is a choice about what shoppers should see first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
