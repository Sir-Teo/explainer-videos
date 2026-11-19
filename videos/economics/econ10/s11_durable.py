from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

CRUSOE = island.CAST["crusoe"].color


class Durable(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Durable goods and the Coase conjecture", r"Can a monopolist of a good that lasts charge a "
             r"monopoly price?", "Chapter nine. Durable goods and the Coase conjecture.", lit={1972: r"Coase on durability"},
             horizon=("a year", "a decade"))
        self.temptation()
        self.prices()
        self.remedies()

    def temptation(self):
        rows = VGroup(
            label(r"Crusoe sells boats, \ which last; \ buyers value one at \$0 to \$1{,}000, \ evenly spread",
                  font_size=25),
            label(r"a one-off monopoly price: \ \$500, \ sold to the top half", font_size=25, color=PROFIT),
            label(r"next season, \ the buyers below \$500 are still there: \ why not sell to them at less?",
                  font_size=25),
            label(r"buyers know it, \ so even eager ones wait for the cut", font_size=25, color=HOLD),
            label(r"Crusoe competes with his own future self", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4)
        tag = published_tag(r"Coase, Journal of Law and Economics 15(1) (1972)", corner=DR, font_size=14)
        with self.voiceover(
            "In 1972 Ronald Coase noticed a problem for any monopolist of something that lasts. "
            "<bookmark mark='a'/> Crusoe now sells boats, which last for years. Buyers value one at anything from "
            "nothing to a thousand dollars, evenly spread. <bookmark mark='b'/> Selling once, his best price would "
            "be five hundred dollars, to the top half. <bookmark mark='c'/> But next season the buyers who valued a "
            "boat at less than five hundred are still there, and selling to them at a lower price would earn him "
            "more. <bookmark mark='d'/> The buyers know it. So even buyers who would pay five hundred wait for the "
            "cut. <bookmark mark='e'/> Crusoe is competing with his own future self, and the faster he can cut his "
            "price, the fiercer that competition is."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def prices(self):
        d = load("durable")
        rows = d["rows"]
        ax = plane([-0.6, 4.6], [0, 0.55], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], xlabel=r"price changes a year",
                   ylabel=r"first price, \ \$ thousands", font_size=17,
                   xfmt=lambda v: {0: "1", 1: "4", 2: "12", 3: "52", 4: "365"}.get(int(round(v)), ""))
        a = ax.ax
        static = DashedLine(a.c2p(-0.6, 0.5), a.c2p(4.6, 0.5), color=PROFIT, stroke_width=2)
        sl = label(r"monopoly price, \ selling once", font_size=18, color=PROFIT).next_to(a.c2p(2.0, 0.5), UP,
                                                                                         buff=0.08)
        bars = VGroup(*[Rectangle(width=0.5, height=max(a.c2p(0, r["first_price"])[1] - a.c2p(0, 0)[1], 1e-3),
                                  stroke_width=0, fill_color=CRUSOE, fill_opacity=0.85).move_to(a.c2p(k, 0),
                                                                                              aligned_edge=DOWN)
                        for k, r in enumerate(rows)])
        nums = VGroup(*[label(rf"\${1000 * r['first_price']:.0f}", font_size=18, color=CRUSOE).next_to(b, UP,
                                                                                                    buff=0.06)
                        for b, r in zip(bars, rows)])
        side = VGroup(
            label(r"Agora: \ buyers who can wait, \ a seller who can't commit, \\ 10\% a year discounting, \ thirty "
                  r"years of selling", font_size=21),
            label(rf"one price change a year: \ the first price is \${1000 * rows[0]['first_price']:.0f}", font_size=22,
                  color=CRUSOE),
            label(rf"daily: \ \${1000 * rows[-1]['first_price']:.0f}", font_size=22, color=CRUSOE),
            label(r"as price changes come faster, \ the price falls toward cost: \\ the Coase conjecture", font_size=22,
                  color=E.ACCENT),
            label(r"proved in versions by Stokey (1981), \ Bulow (1982), \\ and Gul, Sonnenschein and Wilson (1986)",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora solves the game: buyers who can wait, a seller who can't promise not to cut, money discounted at "
            "ten percent a year, and thirty years of selling. <bookmark mark='a'/> If Crusoe can change his price "
            "only once a year, his first price is two hundred and thirty-nine dollars, less than half the one-off "
            "monopoly price. <bookmark mark='b'/> Quarterly, a hundred and thirty-nine; monthly, eighty-eight; "
            "weekly, forty-nine; daily, thirty. <bookmark mark='c'/> The more often he can cut, the lower his "
            "price starts, heading toward his cost. Coase conjectured that in the limit a monopolist of a durable "
            "good has no power at all, <bookmark mark='d'/> and versions of the conjecture were proved by Nancy "
            "Stokey, Jeremy Bulow, and Faruk Gul, Hugo Sonnenschein and Robert Wilson."
        ) as vo:
            self.play(FadeIn(ax), Create(static), FadeIn(sl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(nums[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:]], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(n_) for n_ in nums[1:]], lag_ratio=0.4), FadeIn(side[2]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def remedies(self):
        head = label(r"how a durable-goods monopolist fights back", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"rent instead of sell: \ a renter has no future self to compete with", font_size=25),
            label(r"commit: \ limited editions, \ broken moulds, \ a promise to refund the difference", font_size=25),
            label(r"make it last less: \ planned obsolescence (Bulow, 1986)", font_size=25),
            label(r"build a reputation for not cutting", font_size=25),
            label(r"the general lesson: \ market power needs commitment, \ and time erodes it", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So a monopolist of something durable looks for ways to tie its own hands. <bookmark mark='a'/> It can "
            "rent instead of selling: a firm that rents has no future self to compete with. <bookmark mark='b'/> It "
            "can commit: limited editions, moulds destroyed after a print run, a promise to refund the difference to "
            "earlier buyers if the price falls. <bookmark mark='c'/> It can make the good last less, as Jeremy Bulow "
            "argued in 1986. <bookmark mark='d'/> Or it can build a reputation for never cutting. "
            "<bookmark mark='e'/> The general lesson: market power needs commitment, and time erodes it."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
