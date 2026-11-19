from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

AC = "#F2A65A"
VAR = "#C9A0FF"


class Variety(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Monopolistic competition", r"What if there are many firms, \ but each sells something a "
             r"little different?", "Chapter six. Monopolistic competition.", lit={1933: r"Chamberlin and Robinson"},
             scale=("firm", "market", "nation"), horizon=("a year", "a decade"))
        self.chamberlin()
        self.dixit()
        self.scale()

    def chamberlin(self):
        v = load("variety")
        xs = np.linspace(0.8, 9.0, 120)
        ac = v["c"] + v["f"] / xs
        dem = v["p"] * (xs / v["x"]) ** (-1 / v["sigma"])
        ax = plane([0, 9.2], [0.8, 2.4], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 3, 6, 9], yticks=[1, 4 / 3, 2], xlabel=r"one baker's loaves a day (hundreds)",
                   ylabel=r"price, \ \$", font_size=16, xfmt=lambda v_: f"{v_:.0f}",
                   yfmt=lambda v_: {1: "1", 4 / 3: "1.33", 2: "2"}.get(v_, f"{v_:.2f}"))
        a = ax.ax
        acc = path(ax, xs, ac, color=AC, width=3.5, yr=(0.8, 2.4))
        acl = label(r"average cost", font_size=16, color=AC).next_to(a.c2p(1.2, 1.9), RIGHT, buff=0.1)
        dc = path(ax, xs, dem, color=WHITE, width=3.5, yr=(0.8, 2.4))
        dl = label(r"her demand", font_size=16).next_to(a.c2p(8.0, float(v["p"] * (8 / v["x"]) ** -0.25)), UP,
                                                        buff=0.1)
        mc = DashedLine(a.c2p(0, v["c"]), a.c2p(9.2, v["c"]), color=COMPETE, stroke_width=2)
        mcl = label(r"marginal cost", font_size=15, color=COMPETE).next_to(a.c2p(7.0, v["c"]), DOWN, buff=0.08)
        tan = Dot(a.c2p(v["x"], v["p"]), radius=0.09, color=EQ)
        side = VGroup(
            label(r"Edward Chamberlin \ and Joan Robinson, \\ both in 1933", font_size=21),
            label(r"many bakers, \ each loaf a little different: \\ each baker faces her own sloping demand",
                  font_size=21),
            label(r"while profits last, \ new bakers open, \\ and each one's demand shrinks", font_size=21,
                  color=GREY_A),
            label(r"until demand just touches average cost: \\ price above marginal cost, \ yet zero profit",
                  font_size=21, color=EQ),
            label(r"each bakery runs below its cheapest scale: \\ the price of variety", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Chamberlin, \emph{The Theory of Monopolistic Competition} (1933); \ Robinson, "
                            r"\emph{The Economics of Imperfect Competition} (1933)", corner=DR, font_size=12)
        with self.voiceover(
            "Most markets with many sellers are not like Part nine's either. <bookmark mark='a'/> In 1933 two books "
            "appeared in the same year, by Edward Chamberlin at Harvard and Joan Robinson at Cambridge, "
            "about markets in between. <bookmark mark='b'/> Think of the Island's bakers. There are many, but each "
            "loaf is a little different, so each baker faces her own downward-sloping demand, and sets her own "
            "price. <bookmark mark='c'/> While bakers make profits, new ones open, and each one's demand shrinks. "
            "<bookmark mark='d'/> Entry stops when demand just touches average cost: the price is above marginal "
            "cost, as for a monopoly, yet profit is zero, as under competition. <bookmark mark='e'/> And every "
            "bakery runs below the scale at which bread would be cheapest to make. That is the cost of variety, "
            "and whether variety is worth it is the question the next model answers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(dc), FadeIn(dl), Create(mc), FadeIn(mcl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(acc), FadeIn(acl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(tan, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dixit(self):
        v = load("variety")
        hc = history_card(1977, r"Avinash Dixit and Joseph Stiglitz", r"``Monopolistic Competition and Optimum "
                          r"Product Diversity'': \ Chamberlin's idea, \ made exact", color=VAR, width=11.0,
                          font_size=24).to_edge(UP, buff=0.45)
        eqs = VGroup(
            MathTex(r"U = \Big( \sum_{i=1}^{n} x_i^{\frac{\sigma - 1}{\sigma}} \Big)^{\frac{\sigma}{\sigma - 1}}",
                    font_size=40, color=VAR),
            MathTex(r"p = \frac{\sigma}{\sigma - 1}\, c, \qquad x = \frac{(\sigma - 1) f}{c}, \qquad "
                    r"n = \frac{L}{\sigma f}", font_size=36, color=EQ),
        ).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.45)
        rows = VGroup(
            label(r"$\sigma$: \ how easily one variety replaces another; \ each firm marks up by a fixed ratio",
                  font_size=22),
            label(rf"on the Island, \ $\sigma = {v['sigma']:.0f}$: \ a markup of a third; \ {v['n']:.0f} varieties "
                  rf"for {v['L']:.0f} workers", font_size=22, color=EQ),
            label(r"the model trade, \ growth and macroeconomics borrow: \ Parts 21, \ 30 and 36", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.22).next_to(eqs, DOWN, buff=0.4)
        tag = published_tag(r"Dixit and Stiglitz, AER 67(3) (1977)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1977 Avinash Dixit and Joseph Stiglitz made Chamberlin's idea exact. <bookmark mark='a'/> People "
            "like variety: their utility adds up all the varieties, each raised to a power below one, so a little "
            "of many is better than a lot of one. The parameter sigma measures how easily one variety replaces "
            "another. <bookmark mark='b'/> Then every firm charges the same fixed markup over its marginal cost, "
            "sigma over sigma minus one. Free entry fixes each firm's size, and the number of varieties is "
            "proportional to the size of the economy. <bookmark mark='c'/> With sigma of four, firms mark up by a "
            "third, and an Island of a hundred workers supports twenty-five varieties. <bookmark mark='d'/> Its "
            "simplicity made it the workhorse of three later revolutions: in growth theory, where new varieties "
            "are new ideas; in macroeconomics, where firms that set prices can be slow to change them; and in "
            "trade. Parts twenty-one, thirty and thirty-six use it."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def scale(self):
        v = load("variety")
        Ls = np.array(v["Ls"])
        ns = np.array(v["ns"])
        w = np.array(v["welfare"])
        ax = plane([0, 850], [0, 2.2], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 100, 200, 400, 800], yticks=[0, 0.5, 1, 1.5, 2], xlabel=r"workers in the economy",
                   ylabel=r"well-being per worker \ (100 workers $= 1$)", font_size=16, xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.1f}")
        a = ax.ax
        curve = path(ax, Ls, w, color=VAR, width=3.5)
        dots = VGroup(*[Dot(a.c2p(L, y), radius=0.07, color=VAR) for L, y in zip(Ls, w)])
        side = VGroup(
            label(r"wages, \ prices and firm size don't change \\ as the economy grows; \ only the number \\ of "
                  r"varieties does", font_size=21),
            label(rf"{Ls[2]:.0f} workers: \ {ns[2]:.0f} varieties; \\ {Ls[3]:.0f} workers: \ {ns[3]:.0f}; \ "
                  rf"{Ls[5]:.0f} workers: \ {ns[5]:.0f}", font_size=21, color=VAR),
            label(rf"each worker is better off by $2^{{1/(\sigma - 1)}}$, \\ {w[3]:.2f} times, \ each time the "
                  r"economy doubles", font_size=21, color=EQ),
            label(r"two islands that trade become one bigger island: \\ the gain from trade between similar "
                  r"countries \\ (Krugman, \ 1979; \ Part 36)", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The model holds a surprise. Let the economy grow. <bookmark mark='a'/> Wages, prices and the size of "
            "each firm stay the same. Only the number of varieties changes. <bookmark mark='b'/> A hundred workers "
            "support twenty-five varieties; two hundred, fifty; eight hundred, two hundred. "
            "<bookmark mark='c'/> Because people value variety, each worker is better off by a factor of two to the "
            "power one over sigma minus one, about one point two six, every time the economy doubles. "
            "<bookmark mark='d'/> Two islands that begin to trade become one larger island, with more varieties for "
            "everyone. Paul Krugman used exactly this in 1979 to explain why similar countries trade so much with "
            "each other, the subject of Part thirty-six."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.2),
                      FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
