from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

OFFER = "#F2A65A"


class Centipede(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The centipede and the ultimatum game", r"How far does backward induction go with real "
             r"people?", "Chapter seven. The centipede and the ultimatum game.", lit={1992: r"McKelvey and Palfrey"},
             scale=("person",), horizon=("a day",))
        self.centipede()
        self.ultimatum()

    def centipede(self):
        c = load("centipede")
        takes = c["takes"]
        n = c["moves"]
        xs = [-5.4 + 2.3 * k for k in range(n + 1)]
        y = 1.0
        nodes, edges, downs, leaves = VGroup(), VGroup(), VGroup(), VGroup()
        for k in range(n):
            col = ANA if k % 2 == 0 else BO
            nodes.add(tree_node([xs[k], y, 0], col))
            nxt = [xs[k + 1], y, 0] if k < n - 1 else [xs[n] - 0.25, y, 0]
            edges.add(tree_edge([xs[k], y, 0], nxt, r"pass", col, side=UP, font_size=17))
            downs.add(tree_edge([xs[k], y, 0], [xs[k], y - 1.5, 0], r"take", col, side=LEFT, font_size=17))
            pay = takes[k] if k % 2 == 0 else (takes[k][1], takes[k][0])
            leaves.add(payoff_leaf([xs[k], y - 1.85, 0], [f"{v:.2f}" for v in pay], font_size=21))
        end = takes[n] if n % 2 == 0 else (takes[n][1], takes[n][0])
        leaves.add(payoff_leaf([xs[n] + 0.3, y, 0], [f"{v:.2f}" for v in end], font_size=21))
        who = VGroup(label(r"Ana", font_size=18, color=ANA).next_to(nodes[0], UP, buff=0.35),
                     label(r"Bo", font_size=18, color=BO).next_to(nodes[1], UP, buff=0.35))
        rows = VGroup(
            label(r"each turn, \ the mover can take the larger share of the pot, \ or pass, \ and the pot doubles",
                  font_size=22),
            label(r"at the last turn Bo takes: \ 3.20 beats 1.60; \ so Ana takes the turn before, \ and so back to "
                  r"the start", font_size=22, color=EQ),
            label(r"the subgame-perfect prediction: \ Ana takes at once, \ (0.40, \ 0.10), \ though passing to the "
                  r"end gives (6.40, \ 1.60)", font_size=22, color=HOLD),
            label(r"McKelvey and Palfrey (1992), \ dollars at stake: \ hardly anyone took at the first chance; \ "
                  r"most passed several times", font_size=21, color=LEVEL),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        down_hi = VGroup(*[d[0].copy().set_stroke(EQ, 6) for d in downs])
        tag = published_tag(r"Rosenthal, JET 25 (1981); \ McKelvey and Palfrey, Econometrica 60(4) (1992)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Backward induction is powerful, and sometimes it goes too far. <bookmark mark='a'/> Robert Rosenthal's "
            "centipede game has a pot that doubles every time a player passes. On each turn, the mover can take the "
            "larger share of the pot and end the game, or pass it to the other. <bookmark mark='b'/> Work backward. "
            "At the last turn Bo takes, because three twenty beats the one sixty he would get by passing. Knowing "
            "that, Ana takes at the turn before, and so on, all the way back to the start. "
            "<bookmark mark='c'/> So the only subgame-perfect outcome is that Ana takes at once, and they split forty "
            "cents and ten, when passing to the end would have given them six forty and one sixty. "
            "<bookmark mark='d'/> When Richard McKelvey and Thomas Palfrey ran the game with real money in 1992, "
            "hardly anyone took at the first chance, and most players passed several times."
        ) as vo:
            self.play(FadeIn(nodes), FadeIn(edges), FadeIn(downs), FadeIn(leaves), FadeIn(who), FadeIn(tag),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(d) for d in reversed(down_hi)], lag_ratio=0.5), FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(leaves[0], color=EQ))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ultimatum(self):
        c = load("centipede")
        h = c["henrich"]
        lo, hi = h["mean_offer_range"]
        ax = plane([0, 60], [0, 1], center=LEFT * 2.8 + DOWN * 0.6, x_length=6.6, y_length=1.2,
                   xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[], xlabel=r"mean offer, \ \% of the pie", font_size=16)
        a = ax.ax
        band = Rectangle(width=a.c2p(100 * hi, 0)[0] - a.c2p(100 * lo, 0)[0], height=0.5, stroke_width=0,
                         fill_color=OFFER, fill_opacity=0.6).move_to(a.c2p(100 * (lo + hi) / 2, 0.5))
        bl = label(rf"fifteen small-scale societies: \ {100 * lo:.0f}\% to {100 * hi:.0f}\%", font_size=18,
                   color=OFFER).next_to(band, UP, buff=0.12)
        ind = Dot(a.c2p(100 * h["industrial_mean"], 0.5), radius=0.1, color=WHITE)
        il = label(rf"industrial societies: \ about {100 * h['industrial_mean']:.0f}\%", font_size=18).next_to(
            ind, DOWN, buff=0.35)
        spe = Dot(a.c2p(0.5, 0.5), radius=0.1, color=EQ)
        sl = label(r"subgame perfect: \ the smallest coin", font_size=18, color=EQ).next_to(spe, UP, buff=0.5).shift(
            RIGHT * 0.9)
        rows = VGroup(
            label(r"the ultimatum game: \ Ana proposes how to split \$10; \ Bo accepts, \ or rejects and both get "
                  r"nothing", font_size=22),
            label(r"any offer beats nothing, \ so Bo should accept anything, \ and Ana should offer almost nothing",
                  font_size=22, color=EQ),
            label(r"first run by G\"uth, \ Schmittberger and Schwarze (1982): \ many offered half, \ low offers were "
                  r"rejected",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        side = VGroup(
            label(r"Henrich et al. (2001): \\ the canonical selfish model \\ fits none of the fifteen", font_size=21,
                  color=OFFER),
            label(r"offers were higher where \\ daily life depends more \\ on markets, \ and on \\ "
                  r"cooperating to produce", font_size=20, color=GREY_A),
            label(r"people bring fairness, \\ and anger, \ to games: \\ Part 45", font_size=21, color=LEVEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.4)
        tag = published_tag(r"G\"uth, Schmittberger and Schwarze, JEBO 3(4) (1982); \ Henrich et al., AER 91(2) "
                            r"(2001)", corner=DR, font_size=13)
        with self.voiceover(
            "A two-move game shows the same gap. <bookmark mark='a'/> In the ultimatum game, Ana proposes how to "
            "split ten dollars, and Bo can accept, or reject so that neither gets anything. "
            "<bookmark mark='b'/> Any offer beats nothing, so a selfish Bo accepts anything, and Ana, knowing it, "
            "offers almost nothing. <bookmark mark='c'/> When Werner Güth, Rolf Schmittberger and Bernd Schwarze "
            "first ran the game in 1982, the most common offer was half, and low offers were often rejected. "
            "<bookmark mark='d'/> In 2001 a team of anthropologists and economists led by Joseph Henrich ran it in "
            "fifteen small-scale societies, from foragers to herders. Mean offers ranged from twenty-six to fifty-"
            "eight percent of the pie, against about forty-four in industrial societies, and the selfish prediction "
            "fitted none of them. <bookmark mark='e'/> Offers were higher where daily life depends more on "
            "markets, and on cooperating with others to produce. <bookmark mark='f'/> People bring fairness, and anger, to "
            "games, and Part forty-five takes them seriously."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(ax), FadeIn(spe), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(band), FadeIn(bl), FadeIn(ind), FadeIn(il), FadeIn(side[0]))
            vo.wait_until("e")
            self.play(FadeIn(side[1]))
            vo.wait_until("f")
            self.play(FadeIn(side[2]))
        self.clear_scene()
